import badkeys

from api import dh_w


def main():
    print("Running dh_w tests...")
    test_pubkeys()
    print("All dh_w tests passed")


def test_pubkeys():
    dh_key = dh_w.construct(2048)

    key_info = badkeys.detectandcheck(dh_key.public_key().export_key("PEM").decode())
    assert not key_info.get("results"), f"{key_info.get('results')}"


if __name__ == "__main__":
    main()
