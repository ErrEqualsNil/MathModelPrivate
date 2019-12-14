import autoMachine

if __name__ == "__main__":

    test_time = input("Please input test iterations:")
    test_time = int(test_time)
    total_walk_time = 0
    for i in range(test_time):
        print("\rProcessing : {} / {}".format(i, test_time))
        walktime = autoMachine.process()
        total_walk_time += walktime

    print("Average leave time is {}".format(total_walk_time/test_time))
