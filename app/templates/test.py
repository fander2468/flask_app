how_many_times = int(input("How many times should you watch the video: "))# Mininal 25 times

def rewatch_video(amount_of_times):
    if amount_of_times == 0:
        print("Hey maybe you're good now")
        return 
    else:
	    print(f'You must watch the video {amount_of_times} more times go back and rewatch the video!')
	    rewatch_video(amount_of_times - 1)

print(rewatch_video(how_many_times))