f= open('business.ssv','rU')
data = [line.rstrip('\n') for line in f]

business=[]
for i in range(len(data)):
	temp=data[i].split(' ')
	business.append(temp)
f.close()	
	
f1= open('users.ssv','rU')
data = [line.rstrip('\n') for line in f1]

users=[]
for i in range(len(data)):
	temp=data[i].split(' ')
	users.append(temp)
	
f1.close()


f2= open('xaa','rU')
data = [line.rstrip('\n') for line in f2]

reviews=[]
for i in range(len(data)):
	temp=data[i].split(' ')
	reviews.append(temp)
	
f2.close()

tempsum=0
for i in range(len(business)):
	tempsum=tempsum+float(business[i][1])
mu=tempsum/len(business)
print 'mu is '+str(mu)

match=0
total_reviews_used=0
for i in range(len(reviews)):
	users_temp=reviews[i][0]
	business_temp=reviews[i][1]
	stars_temp=reviews[i][2]
	flag_users=False
	flag_business=False
	for j in range(len(business)):
		if business_temp==business[j][0]:
			flag_business=True
			break
	if flag_business:
		for k in range(len(users)):
			if users_temp==users[k][0]:
				flag_users=True
				break
		if flag_users:
			star_calc=mu+(float("{0:.3f}".format(float(users[k][1])))-mu)+(float(business[j][1])-mu)
			star_calc=int(round(star_calc))
			if star_calc>5:
				star_calc=5
	if flag_users:
		total_reviews_used=total_reviews_used+1
		if str(star_calc)==str(stars_temp):
			match=match+1

accuracy = float(match)/float(total_reviews_used)
print 'total = '+str(total_reviews_used)
print 'correct prediction = '+str(match)
print 'accuracy = '+str(accuracy)			








		
			











