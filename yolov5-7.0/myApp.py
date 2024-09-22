import os
import json
from flask import Flask,request,jsonify,send_file
import torch
from models.common import DetectMultiBackend
from utils.general import non_max_suppression,scale_boxes,check_img_size,increment_path
from utils.augmentations import letterbox
import cv2
import numpy as np
from flask_cors import CORS
from pathlib import Path
from utils.torch_utils import select_device,time_sync
from utils.plots import Annotator,colors
from utils.dataloaders import LoadImages
import mimetypes

app = Flask(__name__)
CORS(app, resources={r'/*': {"origin": "*"}})

device = select_device('')
model = DetectMultiBackend('runs/train/exp3/weights/best.pt',device=device)
stride, names, pt = model.stride, model.names, model.pt

UPLOAD_FOLDER = 'uploads'
RESULT_FOLDER = 'results'
os.makedirs(UPLOAD_FOLDER,exist_ok=True)
os.makedirs(RESULT_FOLDER,exist_ok=True)

def draw_boxes(image, predictions, names):
    annotator = Annotator(image, line_width=2, example=str(names))
    for det in predictions:
        if det is not None and len(det):
            for *xyxy, conf, cls in reversed(det):
                label = f'{names[int(cls.item())]} {conf.item():.2f}'
                annotator.box_label(xyxy, label, color= colors(int(cls.item()),True))
    return annotator.result()

def detect_image(image_path, save_path):
    img = cv2.imread(image_path)
    img = letterbox(img, 640, stride=32, auto=True)[0]
    img0 = img.copy()
    img = img.transpose((2,0,1))[::-1]
    img = np.ascontiguousarray(img)
    img = torch.from_numpy(img).to(device)
    img = img.float()
    img /= 255.0
    if img.ndimension() == 3:
        img = img.unsqueeze(0)

    pred = model(img,augment=False,visualize=False)
    pred = non_max_suppression(pred,0.25,0.45,None,False,max_det=1000)

    results = []
    wheat_count = 0
    img0 = draw_boxes(img0,pred,names)
    for det in pred:
        if det is not None and len(det):
            wheat_count += len(det)
            for *xyxy, conf, cls in reversed(det):
                results.append({
                    'bbox': [int(x) for x in xyxy],
                    'confidence': float(conf),
                    'class': int(cls),
                    'class_name': names[int(cls)]
                })
    cv2.imwrite(save_path, img0)

    data_filename = f"{os.path.splitext(os.path.basename(image_path))[0]}.json"
    data_filepath = os.path.join(os.path.dirname(save_path), data_filename)
    with open(data_filepath, 'w') as f:
        json.dump(results,f)

    return results,wheat_count,data_filename

def detect_video(video_path, save_path):
    source = video_path
    save_dir = Path(save_path)

    dataset = LoadImages(source, img_size=640, stride=stride, auto=pt)
    bs = 1

    model.warmup(imgsz=(1 if pt else bs, 3, 640, 640))
    dt, seen = [0.0, 0.0, 0.0], 0
    vid_path, vid_writer = None, None

    video_results = []

    for path, img, im0s, vid_cap, s in dataset:
        t1 = time_sync()
        img = torch.from_numpy(img).to(device)
        img = img.float()
        img /= 255
        if len(img.shape) == 3:
            img = img[None]
        t2 = time_sync()
        dt[0] += t2 - t1

        pred = model(img, augment=False, visualize = False)
        t3 = time_sync()
        dt[1] += t3 - t1

        pred = non_max_suppression(pred, 0.25, 0.45, None, False, max_det=1000)
        dt[2] += time_sync() - t3

        pred = non_max_suppression(pred,0.25,0.45,None, False, max_det=1000)
        dt[2] += time_sync() - t3

        for i, det in enumerate(pred):
            seen += 1
            p, im0 = path, im0s.copy()

            p = Path(p)
            save_path = str(save_dir / p.name)
            txt_path = str(save_dir / 'labels' / p.stem) +('' if dataset.mode == 'image' else f'_{dataset.frame}')

        frame_results = []
        if det is not None and len(det):
            im0 = draw_boxes(im0, [det], names)
            for *xyxy, conf, cls in reversed(det):
                frame_results.append({
                    'frame': dataset.frame,
                    'bbox': [int(x) for x in xyxy],
                    'confidence': float(conf),
                    'class': int(cls),
                    'class_name': names[int(cls)]
                })
        video_results.append(frame_results)

        if dataset.mode == 'image':
            cv2.imwrite(save_path, im0)
        else:
            if vid_path != save_path:
                vid_path = save_path
                if isinstance(vid_writer, cv2.VideoWriter):
                    vid_writer.release()
                if vid_cap:
                    fps = vid_cap.get(cv2.CAP_PROP_FPS)
                    w = int(vid_cap.get(cv2.CAP_PROP_FRAME_WIDTH))
                    h = int(vid_cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
                else:
                    fps, w, h = 30, im0.shape[1], im0.shape[0]
                save_path = str(Path(save_path).with_suffix('.mp4'))
                fourcc = cv2.VideoWriter(*'avc1')
                vid_writer = cv2.VideoWriter(save_path,fourcc, fps, (w, h))
            vid_writer.write(im0)

    data_filename = f"{Path(video_path).stem}.json"
    data_filepath = os.path.join(save_dir , data_filename)
    with open(data_filepath, 'w') as f:
        json.dump(video_results, f)
    t = tuple(x / seen * 1E3 for x in dt)
    print(f'Speed:{t[0]:.1f}ms pre-process, {t[1]:.1f}ms inference, {t[2]:.1f}ms NMS per image at shape {(1,3,640,640)}')

@app.route('/upload/image', methods=['POST'])
def upload_image():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'})
    file = request.files['file']

    if file.filename == '':
        return jsonify({'error':'No selected file'})

    filename = file.filename
    print("filename: {}".format(filename))
    filepath = os.path.join(UPLOAD_FOLDER,filename)
    file.save(filepath)

    save_path = os.path.join(RESULT_FOLDER, filename)
    results, wheat_count, data_filename = detect_image(filepath, save_path)

    detection_image_url = f'/results/{filename}'
    return jsonify({
        'image_url': detection_image_url,
        'wheat_count': wheat_count,
        'data_url': f'/results/data/{data_filename}'
    })

@app.route('/upload/video', methods=['POST'])
def upload_video():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'})
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'})
    filename = file.filename
    filepath = os.path.join(UPLOAD_FOLDER, filename)
    file.save(filepath)

    video_folder = os.path.join(RESULT_FOLDER, os.path.splitext(filename)[0])
    os.makedirs(video_folder, exist_ok=True)

    detect_video(filepath, video_folder)

    result_files = os.listdir(video_folder)
    video_file = next((f for f in result_files if f.endswith('.mp4')), None)
    json_file = next((f for f in result_files if f.endswith('.json')), None)

    if video_file and json_file:
        video_url = f'/results/{os.path.splitext(filename)[0]}/{video_file}'
        data_url = f'/results/data/{os.path.splitext(filename)[0]}/{json_file}'

        return jsonify({
            'video_url': video_url,
            'data_url': data_url
        })
    else:
        return jsonify({'error': 'Failed to process video'})

@app.route('/results/<path:filename>')
def get_image(filename):
    full_path = os.path.join(RESULT_FOLDER, filename)
    if os.path.isfile(full_path):
        return send_file(full_path, mimetype='image/jpeg')
    else:
        return jsonify({'error': 'File not found'}), 404

@app.route('/results/download/<path:filename>')
def download_image(filename):
    full_path = os.path.join(RESULT_FOLDER, filename)
    if os.path.isfile(full_path):
        mime_type, _ = mimetypes.guess_type(full_path)
        return send_file(full_path, mimetype=mime_type, as_attachment=True, download_name=filename)
    else:
        return jsonify({'error':'File not found'}),404


@app.route('/results/data/<path:filename>')
def get_data(filename):
    full_path = os.path.join(RESULT_FOLDER, filename)
    if os.path.isfile(full_path):
        return send_file(full_path, mimetype='application/json')
    else:
        return jsonify({'error': 'File not found'}), 404

@app.route('/results/video/<path:filename>')
def get_video(filename):
    full_path = os.path.join(RESULT_FOLDER, filename)
    if os.path.isfile(full_path):
        mime_type, _ = mimetypes.guess_type(full_path)
        return send_file(full_path, mimetype=mime_type)
    else:
        return jsonify({'error':'File not found'}), 404

@app.route('/results/download/video/<path:filename>')
def download_video(filename):
    full_path = os.path.join(RESULT_FOLDER, filename)
    if os.path.isfile(full_path):
        mime_type, _ = mimetypes.guess_type(full_path)
        return send_file(full_path, mimetype=mime_type, as_attachment=True, download_name=filename)
    else:
        return jsonify({'error': 'File not found'}), 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)


