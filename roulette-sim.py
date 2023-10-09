import numpy as np

# ref: wiki
COND = {
    'single_zero': '0-32-15-19-4-21-2-25-17-34-6-27-13-36-11-30-8-23-10-5-24-16-33-1-20-14-31-9-22-18-29-7-28-12-35-3-26',
    'double_zero': '0-28-9-26-30-11-7-20-32-17-5-22-34-15-3-24-36-13-1-00-27-10-25-29-12-8-19-31-18-6-21-33-16-4-23-35-14-2',
}


def sim_roulette(cond_seq: str, green_on: bool = False):
    sim_range = get_cond(cond_seq)
    if not green_on:
        sim_range = [x for x in sim_range if x != 0]

    hits = 0
    for i in range(10000):
        outcome = sim_range[np.random.randint(0, 38)]
        if outcome % 2 == 1:
            hits += 1


def sim_agent():
    return None


def run():
    cond_seq = COND['double_zero']
    sim_roulette(cond_seq=cond_seq, green_on=False)


def get_cond(cond_seq: str):
    cond_seq = cond_seq.split('-')
    return [int(x) for x in cond_seq]


if __name__ == '__main__':
    run()

