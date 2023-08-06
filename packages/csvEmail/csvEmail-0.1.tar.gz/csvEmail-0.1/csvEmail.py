#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script for sending emails to multiple recipients based on the contents of
a CSV file plus an email template.
"""

import argparse
import csv
import textwrap
import smtplib
import email
import email.mime.text
import email.mime.multipart
import email.mime.application
import os


__version__ = 0.1


parser = argparse.ArgumentParser(
    prog='csvEmail.py',
    description="""\
Sends emails to multiple recipients listed in a CSV file, filling out a
template based on other values from that row.
"""
)

parser.add_argument(
    'csvFile',
    help="The CSV file to read from. Must have an 'email' column."
)

parser.add_argument(
    'templateFile',
    help="""\
The template file for the email. Format will be called with the row
dictionary using the contents of this file."""
)

parser.add_argument(
    '-S',
    '--SEND',
    action='store_true',
    help="Actually send email (default: print out what would be sent)."
)

parser.add_argument(
    '-v',
    '--verbose',
    action='store_true',
    help="""\
Display full email for each recipient instead of two full examples and
then abbreviated emails."""
)

parser.add_argument(
    '-a', '--attach',
    help="""\
Names a column from the CSV which will contain one or more filenames,
separated by semicolons. Each of the listed files will be attached to
the email sent to the addressee of that row."""
)

parser.add_argument(
    '-s', '--sender',
    required=True,
    help="""\
Sets the email address that will be used as the sender for each message.
This is required."""
)

parser.add_argument(
    '-j', '--subject',
    help="""\
Sets the email subject for all messages. If this isn't used and there is
a 'subject' column, the value in that column in each row will be used
for the message sent by that row. If this isn't provided and there is no
'subject' column, an exception will be raised."""
)

parser.add_argument(
    '-c', '--copy',
    nargs='*',
    help="""\
Adds an email address that will be CC'd on all messages sent. Can be
used multiple times."""
)


def sendEmail(
    fromAddr,
    toAddr,
    subject,
    body,
    ccAddrs=[],
    namesOfFilesToAttach=[]
):
    """
    Function for sending an email. Has some heritage from:

    - [This Stackoverflow post](https://stackoverflow.com/questions/1966073/how-do-i-send-attachments-using-smtp)
    - [This example from the Python documentation](http://docs.python.org/library/email-examples.html)
    """  # noqa
    # Create a text/plain message
    msg = email.mime.multipart.MIMEMultipart()
    msg['From'] = fromAddr
    msg['To'] = toAddr
    msg['Subject'] = subject
    if ccAddrs != []:
        msg['cc'] = ','.join(str(x) for x in ccAddrs)

    # The main body is just another attachment
    msg.attach(email.mime.text.MIMEText(body))

    for fileName in namesOfFilesToAttach:
        path, baseFileName = os.path.split(fileName)
        with open(fileName, 'rb') as inFile:
            attachment = email.mime.application.MIMEApplication(
                inFile.read()
            )
        attachment.add_header(
            'Content-Disposition',
            'attachment',
            filename=baseFileName
        )
        msg.attach(attachment)

    # Send the message via localhost's own SMTP server, but don't
    # include the envelope header.

    # TODO: Options for sending via external SMTP server including
    # authentication...

    server = smtplib.SMTP('localhost')
    # server.set_debuglevel(True)
    server.sendmail(fromAddr, [toAddr] + ccAddrs, msg.as_string())
    server.quit()


if __name__ == "__main__":
    args = parser.parse_args()
    try:
        with open(args.csvFile, 'r') as fin:
            rows = []
            skipped = 0
            for row in csv.DictReader(fin):
                if row.get('email'):
                    rows.append(row)
                else:
                    skipped += 1
    except Exception:
        raise IOError(
            "Unable to read and/or parse CSV file '{args.csvFile}'."
        )

    if len(rows) == 0:
        raise ValueError(
            "CSV file has no rows with valid 'email' values."
        )
    elif len(rows) < skipped:
        print(
            "Warning: more skipped than valid rows. Are you sure your"
            " CSV file is correct?"
        )

    try:
        with open(args.templateFile, 'r') as fin:
            template = fin.read()
    except Exception:
        raise IOError(
            "Unable to read template file '{args.templateFile}'."
        )

    if args.SEND:
        print("Actually sending emails!")
    else:
        print(
            "Dry-run: printing what would be sent without actually"
            " sending anything."
        )

    messages = []
    # Format messages first (so if there's a crash we haven't send
    # some of the emails)
    for row in rows:
        message = template.format(**row)
        address = row['email']
        if args.attach:
            attach = row[args.attach].split(';')
            # Ensure we can read from each attachment (TODO:
            # Something less disastrous if they're pipes?)
            for filename in attach:
                try:
                    with open(filename, 'rb') as check:
                        check.read(1)
                except Exception:
                    raise OSError(
                        f"Unable to access attachment '{filename}'."
                    )
        else:
            attach = []

        if args.subject:
            subject = args.subject
        else:
            if 'subject' not in row:
                raise ValueError(
                    "No global subject specified and this row does"
                    " not have a 'subject' value."
                )
            subject = row['subject']

        messages.append((subject, address, message, attach))

    for i, (subject, address, message, attach) in enumerate(messages):
        if args.SEND:
            print(f"Sending email to '{address}'...", end='')
            sendEmail(
                args.sender,
                address,
                subject,
                message,
                args.copy if args.copy is not None else []
            )
            print(" ...done.")
        else:
            if i <= 1 or args.verbose:
                cc = ', '.join(args.copy) if args.copy else '-none-'
                print(f"""\
Email for '{address}':
From: {args.sender}
CC: {cc}
Subject: {subject}
-----
{message}
-----""")
            else:
                print(
                    textwrap.shorten(
                        f"Email for '{address}' starts: {message}",
                        width=80
                    )
                )
