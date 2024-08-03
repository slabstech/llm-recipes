import os
import torch
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image

from sam2.build_sam import build_sam2_video_predictor
import cv2

HOME = os.getcwd()
print("HOME:", HOME)

def show_mask_on_image(img, mask, obj_id=None, color=(0, 255, 0)):
    # Create a copy of the image to draw on
    img_with_mask = img.copy()
    
    # Find the contours of the mask
    contours, _ = cv2.findContours(mask.astype(np.uint8), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    # Draw the contours on the image
    cv2.drawContours(img_with_mask, contours, -1, color, 2)
    if obj_id is not None:
        # Add the object ID to the image
        cv2.putText(img_with_mask, str(obj_id), (contours[0][0][0][0], contours[0][0][0][1]), cv2.FONT_HERSHEY_SIMPLEX, 1, color, 2)
    return img_with_mask

def show_mask(mask, ax, obj_id=None, random_color=False):
    if random_color:
        color = np.concatenate([np.random.random(3), np.array([0.6])], axis=0)
    else:
        cmap = plt.get_cmap("tab10")
        cmap_idx = 0 if obj_id is None else obj_id
        color = np.array([*cmap(cmap_idx)[:3], 0.6])
    h, w = mask.shape[-2:]
    mask_image = mask.reshape(h, w, 1) * color.reshape(1, 1, -1)
    ax.imshow(mask_image)

def show_points(coords, labels, ax, marker_size=200):
    pos_points = coords[labels==1]
    neg_points = coords[labels==0]
    ax.scatter(pos_points[:, 0], pos_points[:, 1], color='green', marker='*', s=marker_size, edgecolor='white', linewidth=1.25)
    ax.scatter(neg_points[:, 0], neg_points[:, 1], color='red', marker='*', s=marker_size, edgecolor='white', linewidth=1.25)   

def function_2(predictor, video_dir, frame_names, out_director):

    inference_state = predictor.init_state(video_path=video_dir)

    predictor.reset_state(inference_state)
    ann_frame_idx = 0  # the frame index we interact with
    ann_obj_id = 1  # give a unique id to each object we interact with (it can be any integers)

    # Let's add a 2nd positive click at (x, y) = (250, 220) to refine the mask
    # sending all clicks (and their labels) to `add_new_points`
    points = np.array([[980, 500], [980, 500]], dtype=np.float32)
    # for labels, `1` means positive click and `0` means negative click
    labels = np.array([1, 1], np.int32)
    _, out_obj_ids, out_mask_logits = predictor.add_new_points(
        inference_state=inference_state,
        frame_idx=ann_frame_idx,
        obj_id=ann_obj_id,
        points=points,
        labels=labels,
    )

    # run propagation throughout the video and collect the results in a dict
    video_segments = {}  # video_segments contains the per-frame segmentation results
    for out_frame_idx, out_obj_ids, out_mask_logits in predictor.propagate_in_video(inference_state):
        video_segments[out_frame_idx] = {
            out_obj_id: (out_mask_logits[i] > 0.0).cpu().numpy()
            for i, out_obj_id in enumerate(out_obj_ids)
        }

    '''
    vis_frame_stride = 1

    for out_frame_idx in range(0, len(frame_names), vis_frame_stride):
        img = cv2.imread(os.path.join(video_dir, frame_names[out_frame_idx]))
        for out_obj_id, out_mask in video_segments[out_frame_idx].items():
            img = show_mask_on_image(img, out_mask, obj_id=out_obj_id)
        cv2.imwrite(os.path.join(out_director, f'frame_{out_frame_idx}.png'), img)
    # render the segmentation results every few frames
    '''
    vis_frame_stride = 1
    
    plt.close("all")
    for out_frame_idx in range(0, len(frame_names), vis_frame_stride):
        plt.figure(figsize=(6, 4))
        #plt.title(f"frame {out_frame_idx}")
        plt.imshow(Image.open(os.path.join(video_dir, frame_names[out_frame_idx])))
        for out_obj_id, out_mask in video_segments[out_frame_idx].items():
            show_mask(out_mask, plt.gca(), obj_id=out_obj_id)
        plt.axis("off")
        plt.savefig(os.path.join(out_director, f'frame_{out_frame_idx}.png'))
    predictor.reset_state(inference_state)
    plt.close("all")
    

def merge_frames_into_video(frame_dir, output_video_path, fps=30):
    # Get a list of all image files in the directory
    frame_files = [f for f in os.listdir(frame_dir) if f.endswith('.jpg') or f.endswith('.png')]
    frame_files.sort()  # Sort the files to ensure they are in the correct order

    # Read the first frame to get the frame size
    first_frame = cv2.imread(os.path.join(frame_dir, frame_files[0]))
    height, width, _ = first_frame.shape

    # Define the codec and create a VideoWriter object
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(output_video_path, fourcc, fps, (width, height))

    # Loop through the frames and write them to the video
    for frame_file in frame_files:
        frame = cv2.imread(os.path.join(frame_dir, frame_file))
        out.write(frame)

    # Release the VideoWriter object
    out.release()

def main():
    # use bfloat16 for the entire notebook
    torch.autocast(device_type="cuda", dtype=torch.bfloat16).__enter__()

    if torch.cuda.get_device_properties(0).major >= 8:
        # turn on tfloat32 for Ampere GPUs (https://pytorch.org/docs/stable/notes/cuda.html#tensorfloat-32-tf32-on-ampere-devices)
        torch.backends.cuda.matmul.allow_tf32 = True
        torch.backends.cudnn.allow_tf32 = True

    sam2_checkpoint = "checkpoints/sam2_hiera_tiny.pt"
    model_cfg = "sam2_hiera_t.yaml"

    predictor = build_sam2_video_predictor(model_cfg, sam2_checkpoint)

        # `video_dir` a directory of JPEG frames with filenames like `<frame_index>.jpg`
    video_dir = "videos/video-720-part1/"

    # scan all the JPEG frame names in this directory
    frame_names = [
        p for p in os.listdir(video_dir)
        if os.path.splitext(p)[-1] in [".jpg", ".jpeg", ".JPG", ".JPEG"]
    ]
    frame_names.sort(key=lambda p: int(os.path.splitext(p)[0]))

    out_director = "videos/output_720_1"
    function_2(predictor, video_dir, frame_names, out_director )

    merge_frames_into_video(out_director, 'output_video.mp4', fps=2)

if __name__ == "__main__":
    main()