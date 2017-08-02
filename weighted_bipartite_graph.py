import math
f= open('business.ssv','rU')
data = [line.rstrip('\n') for line in f]

business=[]
for i in range(len(data)):
	temp=data[i].split(' ')
	temp=map(int,temp)
	business.append(temp)
f.close()	
	
f1= open('users.ssv','rU')
data = [line.rstrip('\n') for line in f1]

users=[]
for i in range(len(data)):
	temp=data[i].split(' ')
	temp=map(int,temp)
	users.append(temp)
	
f1.close()


f2= open('xaa','rU')
data = [line.rstrip('\n') for line in f2]

reviews=[]
for i in range(len(data)):
	temp=data[i].split(' ')
	temp=map(int,temp)
	reviews.append(temp)
	
f2.close()

tempsum=0
match=0
total_reviews_used=0
square_error=0
absolute_error=0

def reccomendation_power(a,b,c,d):
	total_business_rating=0
	total_user_rating=0
	toreturn=0
	
	for o in range(len(reviews)):
	
		if reviews[o][0]==a:	
			total_user_rating=total_user_rating+reviews[o][2]
	for p in range(len(business)):
		total_business_rating=0
		for q in range(len(reviews)):
			if reviews[q][1]==business[p]:
				total_business_rating=total_business_rating+reviews[o][2]
		
		toreturn=toreturn+((c*d)/(total_user_rating*total_business_rating))
			
			
	return toreturn

for i in range(len(reviews)):
	user=reviews[i][0]
	business_t=reviews[i][1]
	rating_given=reviews[i][2]
	flag_users=False
	flag_business=False
	common_users=[]
	common_users_rating=[]
	rating=0
	for h in range(len(users)):
		if users[h][0]==user:
			user_rating_avg=users[h][1]
			break
	print business		
	for j in range(len(business)):
		if business_t==business[j][0]:
			flag_business=True
			break
	if flag_business:
		for k in range(len(users)):
			if user==users[k][0]:
				flag_users=True
				break
		if flag_users:
			for l in range(len(reviews)):
				if reviews[l][1]==business_t:
					common_users.append(reviews[l][0])
					common_users_rating.append(reviews[l][2])
			for m in range(len(common_users)):
				similarity=reccomendation_power(user,business_t,rating_given,common_users_rating[m])
				for n in range(len(users)):
					if common_users[m]==users[n][0]:
						this_user_avg=users[n][1]
						break
				rating=rating+(similarity*(common_users_rating[m]-this_user_avg))
	
	rating_temp=user_rating_avg+rating
	square_error=square_error+(rating_given-rating_temp)*(rating_given-rating_temp)
	absolute_error=absolute_error+abs(rating_given-rating_temp)
	
	
root_mean_square_error=math.sqrt((square_error)/len(reviews))
mean_absolute_error=(absolute_error/len(reviews))
print "the root_mean_square_error is "+str(root_mean_square_error)


		
			











