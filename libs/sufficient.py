import time


def measure_contraction():
    contractions = []
    while True:
        input("진통이 시작되면 엔터를 눌러주세요.")
        start = time.time()
        input("진통이 끝나면 엔터를 눌러주세요.")
        end = time.time()
        duration = end - start
        intensity = int(input("진통의 강도를 1~10까지의 숫자로 평가해주세요."))
        contractions.append((start, duration, intensity))
        print(f"이번 진통은 {duration}초 걸렸으며, 진통의 강도는 {intensity}입니다.")

        if len(contractions) > 1:
            interval = contractions[-1][0] - contractions[-2][0]
            print(f"이전 진통과의 간격은 {interval}초입니다.")

            if interval <= 300 and duration >= 50 and intensity >= 5:
                print("진진통으로 판단됩니다. 병원에 가보는 것을 권장합니다.")
            elif interval <= 300 and duration < 50:
                print("진진통으로 의심됩니다.")
            else:
                print("아직 가진통의 단계로 보입니다.")