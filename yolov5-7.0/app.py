import os
import json
from flask import Flask, request, jsonify, send_file
import torch
from models.common import DetectMultiBackend
from utils.general import non_max_suppression, scale_boxes, check_img_size, increment_path
from utils.augmentations import letterbox
import cv2
import numpy as np
from flask_cors import CORS
from pathlib import Path
from utils.torch_utils import select_device, time_sync
from utils.plots import Annotator, colors
from utils.dataloaders import LoadImages
import mimetypes

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

# 初始化Flask和模型
device = select_device('')
model = DetectMultiBackend('runs/train/13cBest.pt', device=device)  # Load your trained model
stride, names, pt = model.stride, model.names, model.pt

UPLOAD_FOLDER = 'uploads'
RESULT_FOLDER = 'results'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(RESULT_FOLDER, exist_ok=True)


def draw_boxes(image, predictions, names):
    annotator = Annotator(image, line_width=2, example=str(names))
    for det in predictions:
        if det is not None and len(det):
            for *xyxy, conf, cls in reversed(det):
                label = f'{names[int(cls.item())]} {conf.item():.2f}'
                annotator.box_label(xyxy, label, color=colors(int(cls.item()), True))
    return annotator.result()


def detect_video(video_path, save_path):
    source = video_path
    # save_dir = increment_path(Path(save_path) / Path(video_path).stem, mkdir=True)  # increment run
    save_dir = Path(save_path)  # No increment_path here

    # Dataloader
    dataset = LoadImages(source, img_size=640, stride=stride, auto=pt)
    bs = 1  # batch_size

    # Run inference
    model.warmup(imgsz=(1 if pt else bs, 3, 640, 640))  # warmup
    dt, seen = [0.0, 0.0, 0.0], 0
    vid_path, vid_writer = None, None

    video_results = []

    for path, img, im0s, vid_cap, s in dataset:
        t1 = time_sync()
        img = torch.from_numpy(img).to(device)
        img = img.float()  # uint8 to fp16/32
        img /= 255  # 0 - 255 to 0.0 - 1.0
        if len(img.shape) == 3:
            img = img[None]  # expand for batch dim
        t2 = time_sync()
        dt[0] += t2 - t1

        # Inference
        pred = model(img, augment=False, visualize=False)
        t3 = time_sync()
        dt[1] += t3 - t2

        # NMS
        pred = non_max_suppression(pred, 0.25, 0.45, None, False, max_det=1000)
        dt[2] += time_sync() - t3

        # Process predictions
        for i, det in enumerate(pred):  # per image
            seen += 1
            p, im0 = path, im0s.copy()

            p = Path(p)  # to Path
            save_path = str(save_dir / p.name)  # img.jpg
            txt_path = str(save_dir / 'labels' / p.stem) + (
                '' if dataset.mode == 'image' else f'_{dataset.frame}')  # img.txt

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

            # Save results (image with detections)
            if dataset.mode == 'image':
                cv2.imwrite(save_path, im0)
            else:  # 'video' or 'stream'
                if vid_path != save_path:  # new video
                    vid_path = save_path
                    if isinstance(vid_writer, cv2.VideoWriter):
                        vid_writer.release()  # release previous video writer
                    if vid_cap:  # video
                        fps = vid_cap.get(cv2.CAP_PROP_FPS)
                        w = int(vid_cap.get(cv2.CAP_PROP_FRAME_WIDTH))
                        h = int(vid_cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
                    else:  # stream
                        fps, w, h = 30, im0.shape[1], im0.shape[0]
                    save_path = str(Path(save_path).with_suffix('.mp4'))  # force *.mp4 suffix on results videos


                    # vid_writer = cv2.VideoWriter(save_path, cv2.VideoWriter_fourcc(*'mp4v'), fps, (w, h))
                    # Use 'avc1' codec for better compatibility
                    fourcc = cv2.VideoWriter_fourcc(*'avc1')
                    vid_writer = cv2.VideoWriter(save_path, fourcc, fps, (w, h))
                vid_writer.write(im0)

    # Save detection data to JSON file
    data_filename = f"{Path(video_path).stem}.json"
    data_filepath = os.path.join(save_dir, data_filename)
    with open(data_filepath, 'w') as f:
        json.dump(video_results, f)

    # Print results
    t = tuple(x / seen * 1E3 for x in dt)  # speeds per image
    print(
        f'Speed: {t[0]:.1f}ms pre-process, {t[1]:.1f}ms inference, {t[2]:.1f}ms NMS per image at shape {(1, 3, 640, 640)}')


@app.route('/upload/image', methods=['POST'])
def upload_image():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'})

    file = request.files['file']

    if file.filename == '':
        return jsonify({'error': 'No selected file'})

    filename = file.filename
    print("filename: {}".format(filename))
    filepath = os.path.join(UPLOAD_FOLDER, filename)
    file.save(filepath)

    # 使用opencv读取图像,将图像加载为一个Numpy数组
    img = cv2.imread(filepath)
    img = letterbox(img, 640, stride=32, auto=True)[0]
    img0 = img.copy()
    img = img.transpose((2, 0, 1))[::-1]#转化成Pytorch期望的输入格式：CHW。
    img = np.ascontiguousarray(img)
    img = torch.from_numpy(img).to(device)#转化成张量并送入GPU
    img = img.float()
    img /= 255.0
    if img.ndimension() == 3:
        img = img.unsqueeze(0)#图片数据归一化

    pred = model(img, augment=False, visualize=False)#用yolo模型进行预测
    pred = non_max_suppression(pred, 0.25, 0.45, None, False, max_det=1000)#对预测结果进行非极大值抑制

    results = []
    names = model.names

    wheat_count = 0
    img0 = draw_boxes(img0, pred, names)#调用函数绘制检测框
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
    # 遍历每个预测结果，累加麦穗技术，对于有的检测结果，提取边界框坐标，置信度和类别

    detection_image_url = f'/results/{filename}'
    cv2.imwrite(os.path.join(RESULT_FOLDER, filename), img0)#结果保存

    data_filename = f"{os.path.splitext(filename)[0]}.json"#创建一个json文件
    data_filepath = os.path.join(RESULT_FOLDER, data_filename)
    with open(data_filepath, 'w') as f:
        json.dump(results, f)
    #在文件中存储
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
        video_path = os.path.join(video_folder, video_file)
        json_path = os.path.join(video_folder, json_file)
        print(f"Video saved at: {video_path}")  # Debugging
        print(f"JSON saved at: {json_path}")    # Debugging

        # 确保返回的 URL 是相对路径
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
        return send_file(full_path, mimetype='image/jpeg')  # 假设是 JPEG 图像
    else:
        return jsonify({'error': 'File not found'}), 404


@app.route('/results/download/<path:filename>')
def download_image(filename):
    full_path = os.path.join(RESULT_FOLDER, filename)
    if os.path.isfile(full_path):
        mime_type, _ = mimetypes.guess_type(full_path) #采用mimetypes来猜测MIME类型
        print(mime_type)
        print(full_path)
        return send_file(full_path, mimetype=mime_type, as_attachment=True, download_name=filename)
    else:
        return jsonify({'error': 'File not found'}), 404


@app.route('/results/data/<path:filename>')
def get_data(filename):
    full_path = os.path.join(RESULT_FOLDER, filename)
    if os.path.isfile(full_path):
        return send_file(full_path, as_attachment=True, download_name=filename)
    else:
        return jsonify({'error': 'File not found'}), 404

@app.route('/results/video/<path:filename>')
def get_video(filename):
    full_path = os.path.join(RESULT_FOLDER, filename)
    if os.path.isfile(full_path):
        mime_type, _ = mimetypes.guess_type(full_path)
        return send_file(full_path, mimetype=mime_type)
    else:
        return jsonify({'error': 'File not found'}), 404

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
