import cv2
from ultralytics import YOLO

# Load model once (efficient)
vehicle_model = YOLO("yolov8n.pt")

def process_video(input_path, output_path):

    cap = cv2.VideoCapture(input_path)

    fps = cap.get(cv2.CAP_PROP_FPS)
    if fps == 0:
        fps = 30

    # Output writer
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(output_path, fourcc, fps, (800, 600))

    # Parameters
    line_y1 = 250
    line_y2 = 400
    distance_pixels = line_y2 - line_y1
    speed_limit = 20

    vehicle_entry_frame = {}
    frame_count = 0

    def estimate_speed(f1, f2):
        frames = f2 - f1
        if frames <= 0:
            return 0
        time_taken = frames / fps
        speed = (distance_pixels / time_taken) * 0.1
        return speed

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        frame_count += 1
        frame = cv2.resize(frame, (800, 600))

        results = vehicle_model(frame, verbose=False)[0]

        for box in results.boxes:
            x1, y1, x2, y2 = map(int, box.xyxy[0])
            cls = int(box.cls[0])

            if cls in [2, 3, 5, 7]:  # vehicles

                cx = (x1 + x2) // 2
                cy = (y1 + y2) // 2

                obj_id = int(cx / 100)

                # First line
                if cy > line_y1 and obj_id not in vehicle_entry_frame:
                    vehicle_entry_frame[obj_id] = frame_count

                # Second line
                if cy > line_y2 and obj_id in vehicle_entry_frame:
                    entry_frame = vehicle_entry_frame[obj_id]

                    if frame_count - entry_frame > 5:
                        speed = estimate_speed(entry_frame, frame_count)

                        print(f"Vehicle ID: {obj_id} | Speed: {speed:.2f}")

                        if speed > speed_limit:
                            print(f"🚨 OVERSPEEDING → ID: {obj_id}, Speed: {speed:.2f}")

                            cv2.putText(frame, "OVERSPEED!", (x1, y1-10),
                                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,0,255), 2)

                    del vehicle_entry_frame[obj_id]

                cv2.rectangle(frame, (x1,y1), (x2,y2), (0,255,0), 2)

        # Draw lines
        cv2.line(frame, (0, line_y1), (frame.shape[1], line_y1), (255,255,0), 2)
        cv2.line(frame, (0, line_y2), (frame.shape[1], line_y2), (255,255,0), 2)

        # Write frame to output video
        out.write(frame)

    cap.release()
    out.release()

    return output_path