import queue
import threading
import time

# Shared resources
task_queue = queue.Queue(maxsize=5)
event = threading.Event()  # Used to signal threads to stop

# Producer thread
def producer():
    for i in range(10):
        if event.is_set():  # Stop if event is set
            print("[Producer] Stopping...")
            break
        task_queue.put(i)
        print(f"[Producer] Produced item: {i}")
        time.sleep(0.5)  # Simulate work

    print("[Producer] No more items to produce.")

# Consumer thread
def consumer():
    while not event.is_set() or not task_queue.empty():
        try:
            item = task_queue.get(timeout=1)  # Timeout to avoid deadlock
            print(f"[Consumer] Consumed item: {item}")
            task_queue.task_done()
            time.sleep(1)  # Simulate work
        except queue.Empty:
            if event.is_set():
                print("[Consumer] No more items to consume.")
                break

# Controller thread to stop everything after some time
def controller():
    time.sleep(7)  # Let producer and consumer run for a while
    print("[Controller] Stopping threads...")
    event.set()  # Signal threads to stop

# Start threads
producer_thread = threading.Thread(target=producer, name="ProducerThread")
consumer_thread = threading.Thread(target=consumer, name="ConsumerThread")
controller_thread = threading.Thread(target=controller, name="ControllerThread")

producer_thread.start()
consumer_thread.start()
controller_thread.start()

# Wait for threads to finish
producer_thread.join()
consumer_thread.join()
controller_thread.join()

print("[Main] All threads have finished.")