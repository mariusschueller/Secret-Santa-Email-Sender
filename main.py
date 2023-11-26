import csv
import random
import smtplib
from email.mime.text import MIMEText
import personalInfo

giver = []
receiver = []


with open(personalInfo.formName, newline='') as csvfile:
    raw = csv.reader(csvfile, delimiter=',')
    for row in raw:
        # print(row)
        if row[2] == 'Yes! Partner me up!':  # answers yes in the form check
            print(row[1] + " is doing the gift exchange!")
            giver.append(row[1])
            receiver.append(row[1])
        else:
            print("Not partnered up, found: " + row[2])

# print(giver)
# print(receiver)


def getMatchups(giverLst, receiverLst):
    matchups = {}
    while len(giverLst) > 0:

        giverNum = random.randint(0, len(giverLst) - 1)
        receiverNum = random.randint(0, len(receiverLst) - 1)

        # add a check here for if the only person left is the same person and then just restart the process
        while giverLst[giverNum] == receiverLst[receiverNum] or personalInfo.personalRule(giverLst[giverNum], receiverLst[receiverNum]):
            giverNum = random.randint(0, len(giverLst) - 1)
            receiverNum = random.randint(0, len(receiverLst) - 1)

        matchups[giverLst[giverNum]] = receiverLst[receiverNum]  # inclusive
        giverLst.remove(giverLst[giverNum])
        receiverLst.remove(receiverLst[receiverNum])
        # print("Giver list size: " + str(len(giverLst)) + "\nReceiver list size: " + str(len(receiverLst)))

        if len(giverLst) == 1 and len(receiverLst) == 1 and (giverLst[0] == receiverLst[0] or personalInfo.personalRule(giverLst[0], receiverLst[0])):
            print("FAILED")
            return False

    return matchups


# Probably not the most efficient solution, but works well to brute force in this case
res = False
while not res:
    print("Trying to find a pairings")
    giveLst = []
    for person in giver:
        giveLst.append(person)

    receiveLst = []
    for person in receiver:
        receiveLst.append(person)
    res = getMatchups(giveLst, receiveLst)

print("Pairings found!\n")


def send_email(subject, body, sender, recipients, password):
    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = sender
    msg['To'] = ', '.join(recipients)
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp_server:
        smtp_server.login(sender, password)
        smtp_server.sendmail(sender, recipients, msg.as_string())
    print("Email sent!")


for pair in res:
    # Email details
    emailSubject = "ARMADA SECRET SANTA GIFT EXCHANGE!!!"
    emailBody = "Row row row, boats! \n\n"  \
                + "I hope you are all ready to spread some holiday cheer! " \
                  "Your secret Santa partner is none other than the amazing, wonderful: " \
                + personalInfo.nameKey[res[pair]] \
                + ".\n\nThe spending limit on the gift is $15.\n\n" \
                + "Presents will be given at the last practice before finals week/break starts! Happy hunting!" \
                  "\n\nStay chilly,\nSantmada McBoaty"
    emailSender = personalInfo.senderAddress
    emailRecipients = pair
    emailPassword = personalInfo.senderPassword

    # So that it's a secret
    # print(emailBody + "\nSENDING EMAIL TO: " + emailRecipients)
    send_email(emailSubject, emailBody, emailSender, emailRecipients, emailPassword)
print("Finished sending out emails")
