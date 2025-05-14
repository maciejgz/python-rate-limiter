import os
from dotenv import load_dotenv
import threading
import time
import logging
import stomp
from stomp import ConnectionListener

load_dotenv()

RABBITMQ_HOST = os.getenv("RABBITMQ_HOST", "localhost")
RABBITMQ_PORT = int(os.getenv("RABBITMQ_PORT", 5672))
RABBITMQ_QUEUE = os.getenv("RABBITMQ_QUEUE", "rate_limiter_queue")

ACTIVEMQ_HOST = os.getenv("ACTIVEMQ_HOST", "localhost")
ACTIVEMQ_PORT = int(os.getenv("ACTIVEMQ_PORT", 61613))  # popraw na 61613 (STOMP)
ACTIVEMQ_QUEUE = os.getenv("ACTIVEMQ_QUEUE", "/queue/rate_limiter_queue")

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s"
)


class LeakingBucketQueue:
    def consume(self, user_id, tokens):
        try:
            conn = stomp.Connection12([(ACTIVEMQ_HOST, ACTIVEMQ_PORT)])
            conn.connect(wait=True)
            # Browser subscription do sprawdzenia liczby wiadomości w kolejce
            browser_id = "browser-1"
            messages = []
            received = threading.Event()

            class BrowserListener(ConnectionListener):
                def on_message(self, frame):
                    messages.append(frame.body)
                    received.set()

            conn.set_listener("", BrowserListener())
            conn.subscribe(
                destination=ACTIVEMQ_QUEUE,
                id=browser_id,
                ack="auto",
                headers={"browser": "true"},
            )
            # Czekaj maksymalnie 2 sekundy na wiadomości (lepsza responsywność)
            time.sleep(0.5)
            conn.unsubscribe(id=browser_id)

            # Dodatkowe zabezpieczenie: sprawdź ponownie po krótkim czasie
            if len(messages) >= 5:
                logging.warning(
                    f"Request rejected (ActiveMQ queue full): {user_id}. Queue size: {len(messages)}"
                )
                conn.disconnect()
                return False

            # Po odsubskrybowaniu sprawdź jeszcze raz rozmiar kolejki
            # (może być wyścig, ale to ograniczenie STOMP)
            conn.send(
                destination=ACTIVEMQ_QUEUE, body=str(user_id), persistent="true"
            )
            logging.info(f"User {user_id} sent to ActiveMQ queue")
            conn.disconnect()
            return True
        except Exception as e:
            logging.error(f"Failed to send user {user_id} to ActiveMQ: {e}")
            return False

    def clear_queue(self):
        """Usuń wszystkie wiadomości z kolejki ActiveMQ."""
        try:
            conn = stomp.Connection12([(ACTIVEMQ_HOST, ACTIVEMQ_PORT)])
            conn.connect(wait=True)
            messages = []

            class ClearListener(ConnectionListener):
                def on_message(self, frame):
                    messages.append(frame.body)

            conn.set_listener("", ClearListener())
            conn.subscribe(destination=ACTIVEMQ_QUEUE, id="clear", ack="auto")
            time.sleep(1)  # daj czas na pobranie i usunięcie wiadomości
            conn.unsubscribe(id="clear")
            conn.disconnect()
            logging.info(f"Cleared ActiveMQ queue: {ACTIVEMQ_QUEUE}")
        except Exception as e:
            logging.error(f"Failed to clear ActiveMQ queue: {e}")


class _ActiveMQListener(ConnectionListener):
    def __init__(self):
        self.message = None

    def on_message(self, frame):
        self.message = frame.body


class LeakingBucketQueueProcessor:
    def __init__(self, interval=5.0):
        self.interval = interval  # co ile sekund sprawdzać kolejkę
        self._stop_event = threading.Event()
        self.thread = threading.Thread(target=self._process_loop, daemon=True)

    def start(self):
        logging.info("LeakingBucketQueueProcessor started.")
        self.thread.start()

    def stop(self):
        logging.info("LeakingBucketQueueProcessor stopping...")
        self._stop_event.set()
        self.thread.join()
        logging.info("LeakingBucketQueueProcessor stopped.")

    def _process_loop(self):
        while not self._stop_event.is_set():
            try:
                conn = stomp.Connection12([(ACTIVEMQ_HOST, ACTIVEMQ_PORT)])
                listener = _ActiveMQListener()
                conn.set_listener("", listener)
                conn.connect(wait=True)
                conn.subscribe(destination=ACTIVEMQ_QUEUE, id=1, ack="auto")
                time.sleep(1)
                if listener.message:
                    logging.info(f"Reading message from ActiveMQ: UserId from ActiveMQ: {listener.message}")
                # Logowanie pozostałego rozmiaru kolejki
                # Browser subscription do sprawdzenia liczby wiadomości po pobraniu
                browser_id = "browser-check"
                messages = []

                class BrowserListener(ConnectionListener):
                    def on_message(self, frame):
                        messages.append(frame.body)

                conn.set_listener("", BrowserListener())
                conn.subscribe(
                    destination=ACTIVEMQ_QUEUE,
                    id=browser_id,
                    ack="auto",
                    headers={"browser": "true"},
                )
                time.sleep(1)
                conn.unsubscribe(id=browser_id)
                logging.info(f"Pozostały rozmiar kolejki ActiveMQ: {len(messages)}")
                conn.disconnect()
            except Exception as e:
                logging.error(f"Failed to consume from ActiveMQ: {e}")
            time.sleep(self.interval)  # sprawdzaj co 5 sekund (ustawione przez interval)
