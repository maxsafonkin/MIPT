import time
import threading


def pow_seq(pow_: int) -> None:
    result = [i**pow_ for i in range(1, 11)]
    print(f"Pow: {pow_}, result: {result}")


def print_with_timeout() -> None:
    for i in range(1, 11):
        print(i)
        print("Sleeping for 1 second")
        time.sleep(1)


def task_1():
    threads = [threading.Thread(target=pow_seq, args=pow_) for pow_ in [2, 3]]
    for t in threads:
        t.start()

    for t in threads:
        t.join()


def task_2():
    threads = [threading.Thread(target=print_with_timeout) for _ in range(3)]

    for t in threads:
        t.start()

    for t in threads:
        t.join()


def main():
    task_1()
    task_2()


if __name__ == "__main__":
    main()
