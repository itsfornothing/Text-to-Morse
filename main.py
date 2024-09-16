import smtplib
from flask import Flask, render_template, request
from flask_wtf import FlaskForm
from wtforms import FileField, SubmitField
import os


app = Flask(__name__)

app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

morse_library = {
    'A': '.-', 'B': '-...', 'C': '-.-.', 'D': '-..', 'E': '.', 'F': '..-.', 'G': '--.', 'H': '....', 'I': '..',
    'J': '.---', 'K': '-.-', 'L': '.-..', 'M': '--', 'N': '-.', 'O': '---', 'P': '.--.', 'Q': '--.-', 'R': '.-.',
    'S': '...', 'T': '-', 'U': '..-', 'V': '...-', 'W': '.--', 'X': '-..-', 'Y': '-.--', 'Z': '--..', '1': '.----',
    '2': '..---', '3': '...--', '4': '....-', '5': '.....', '6': '-....', '7': '--...', '8': '---..', '9': '----.',
    '0': '-----', ' ': '.......', '!': '-.-.--', '@': '.--.-.', '$': '...-..-', '&': '.-...', '(': '-.--.',
    ')': '-.--.-', '.': '.-.-.-', ',': '--..--', ' " ': '.-..-.', " ' ": ".----.", '/': '-..-.', '?': '..--..',
    '-': '-....-', '_': '..--.-', '+': '.-.-.', '=': '-..-'
}


class UploadFile(FlaskForm):
    file = FileField('File')
    submit = SubmitField('Upload')


@app.route('/', methods=["POST", "GET"])
def home():
    form = UploadFile()
    morse_code = ''
    if request.method == 'POST':
        text = request.form.get('input_text')
        if text:
            for letter in text:
                if letter.upper() in morse_library:
                    morse_code += f'{morse_library[letter.upper()]} '
                else:
                    morse_code += ""
    return render_template('index.html', code=morse_code, form=form)


@app.route('/contact_us', methods=["POST", "GET"])
def contact_us():
    my_gmail = os.getenv('MY_GMAIL')
    password = os.getenv('PASSWORD')
    if request.method == "POST":
        full_name = request.form.get("name")
        email = request.form.get("email")
        message = request.form.get("message")

        with smtplib.SMTP("smtp.gmail.com") as connection:
            connection.starttls()
            connection.login(user=my_gmail, password=password)
            connection.sendmail(from_addr=email,
                                to_addrs=my_gmail,
                                msg=f"Subject:Contact From Text-to-Morse\n\nFull Name: {full_name}\nEmail: "
                                    f"{email}\nMessage: {message}")

    return render_template('contact.html')


if __name__ == '__main__':
    app.run(debug=False)
