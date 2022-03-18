# Python_Email_reverse_shell

This program uses the smtplib and imaplib module to firstly read commands given and send the result/output back to specified email and if specified it can also upload
files that are allowed to be sent on emails.

1. First replace the email and password strings with your original email id and passwords.
2. It will be reading for every incoming emails while it is running.
3. So now you've to send messages to your email which the program will be reading.
4. The basic format is to keep the Subject "command" no capitalizations.
5. And the content or body should contain the command.

Then it will read and execute the command and send you the output back on specified email.
If you send the command starting with "download" followed by the file it will send the file on email.
