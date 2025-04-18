# Author: Elias Mapendo
# Description: Evaluate a trained Faster R-CNN model on both Clear and Foggy Cityscapes datasets

import sys, os, torch, csv, random
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from torch.utils.data import DataLoader, Subset
from models.faster_cnn import get_faster_rcnn_model
from data.datasets import CityscapesDataset
from data.preprocessing import BasicTransform
from torchvision.utils import draw_bounding_boxes
from torchvision.transforms.functional import to_pil_image
from torchvision.ops import box_iou
import matplotlib.pyplot as plt

def collate_fn(batch):
    return tuple(zip(*batch)) if isinstance(batch[0], tuple) else batch


def visualize_and_save_predictions(images, outputs, output_dir, prefix, threshold=0.5):
    os.makedirs(output_dir, exist_ok=True)
    for i, (img, output) in enumerate(zip(images, outputs)):
        boxes = output['boxes'][output['scores'] > threshold]
        labels = output['labels'][output['scores'] > threshold]

        drawn = draw_bounding_boxes((img.cpu() * 255).byte(), boxes, labels=[str(l.item()) for l in labels], colors="red")
        img_pil = to_pil_image(drawn)

        img_path = os.path.join(output_dir, f"{prefix}.png")
        img_pil.save(img_path)


def compute_iou(gt_boxes, pred_boxes, threshold=0.5):
    if len(gt_boxes) == 0 or len(pred_boxes) == 0:
        return 0.0
    ious = box_iou(gt_boxes, pred_boxes)
    matches = (ious > threshold).sum().item()
    return matches / max(len(gt_boxes), 1)


def evaluate_on_split(model, split='val', foggy=False, device='cuda'):
    name = "Foggy" if foggy else "Clear"
    print(f"\n[INFO] Evaluating on {name} Cityscapes ({split})...")

    target_labels = [24, 25, 26, 27, 28, 31, 32, 33]
    num_classes = len(target_labels) + 1

    transform = BasicTransform()
    dataset = CityscapesDataset(
        mode=split, foggy=foggy, transforms=transform, target_labels=target_labels
    )

    indices = random.sample(range(len(dataset)), 50)
    subset = Subset(dataset, indices)
    loader = DataLoader(subset, batch_size=1, shuffle=False, collate_fn=collate_fn)

    model.eval()
    total_iou = 0.0
    imagewise_iou = []
    output_dir = f"outputs/{name.lower()}"
    os.makedirs(output_dir, exist_ok=True)

    with torch.no_grad():
        for idx, batch in enumerate(loader):
            if foggy:
                images = [batch[0].to(device)] if isinstance(batch, tuple) else [b.to(device) for b in batch]
                targets = None
            else:
                images, targets = batch
                images = [img.to(device) for img in images]
                targets = [{k: v.to(device) for k, v in t.items()} for t in targets]

            outputs = model(images)
            visualize_and_save_predictions(images, outputs, output_dir, prefix=f"{name.lower()}_{idx + 1}")

            if not foggy:
                gt_boxes = targets[0]['boxes']
                pred_boxes = outputs[0]['boxes'][outputs[0]['scores'] > 0.5]
                iou = compute_iou(gt_boxes, pred_boxes)
                total_iou += iou
                imagewise_iou.append((f"img_{idx+1}", iou))

    if not foggy:
        avg_iou = total_iou / len(subset)
        print(f"[INFO] Average IoU on {name} set: {avg_iou:.4f}")

        # Save to CSV
        csv_path = os.path.join(output_dir, f"{name.lower()}_iou_report.csv")
        with open(csv_path, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['Image', 'IoU'])
            writer.writerows(imagewise_iou)
            writer.writerow(['Average', avg_iou])

        # Plot bar chart
        plt.figure(figsize=(10, 5))
        plt.bar([x[0] for x in imagewise_iou], [x[1] for x in imagewise_iou], color='skyblue')
        plt.axhline(avg_iou, color='red', linestyle='--', label=f'Average IoU: {avg_iou:.2f}')
        plt.xlabel('Image')
        plt.ylabel('IoU')
        plt.title(f'{name} Image-wise IoU')
        plt.legend()
        plt.tight_layout()
        plt.savefig(os.path.join(output_dir, f"{name.lower()}_iou_chart.png"))
        plt.close()
    else:
        print("[WARN] Skipping IoU: annotations not available for foggy set.")


def evaluate_model(model_path, device='cuda'):
    target_labels = [24, 25, 26, 27, 28, 31, 32, 33]
    num_classes = len(target_labels) + 1

    model = get_faster_rcnn_model(num_classes=num_classes)
    model.load_state_dict(torch.load(model_path, map_location=device))
    model.to(device)

    evaluate_on_split(model, split='val', foggy=False, device=device)
    evaluate_on_split(model, split='val', foggy=True, device=device)


if __name__ == '__main__':
    device = 'cuda' if torch.cuda.is_available() else 'cpu'
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    evaluate_model(
        model_path=os.path.join(project_root, "experiments", "faster_rcnn_cityscapes.pth"),
        device=device)