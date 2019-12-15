import autoMachine
import Astar
import NormalBFSMethod


if __name__ == "__main__":
    test_time = input("Please input test iterations:")
    test_time = int(test_time)
    for i in range(test_time):
        x, y, m = Astar.processMsg()
        walktime = autoMachine.process(x, y, m)
        walktimeByBFS = NormalBFSMethod.process(x,y,m)
        print("Processing : {} / {} - Use {} iterations".format(i, test_time, walktime), flush=True, end="\n")
        print("Time reduce : {}".format((walktimeByBFS - walktime)/walktimeByBFS))

