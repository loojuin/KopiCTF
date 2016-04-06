from flask import Flask, request, render_template
import random

def collate(int_array):
	buf = []
	for b in range(8):
		for i in int_array:
			buf.append((i >> b) & 0b1)
	return buf

def invert_alternate(int_array):
	state = False
	for i in range(len(int_array)):
		if state:
			int_array[i] ^= 1
		state = not state

def chunk(int_array, size):
	if len(int_array) % size != 0:
		raise Exception("chunk(): Array length not compatible with chunk size.")
	retval = []
	for i in range(len(int_array) / size):
		retval.append(int_array[(size * i):(size * (i + 1))])
	return retval

def encode(ip):
	if len(ip) > 256:
		print "String too long."
		return "String too long."
	length = collate([len(ip)])
	length.reverse()
	int_array = [ord(c) for c in ip]
	buf = collate(int_array)
	for i in range(4096 - len(buf) - len(length)):
		buf.append(0 if random.random() > 0.5 else 1)
	buf.extend(length)
	invert_alternate(buf)
	mat = chunk(buf, 64)
	return mat

app = Flask(__name__)

@app.route('/')
def my_form():
	return render_template("my-form.html")

@app.route('/', methods=['POST'])
def my_form_post():
	text = request.form['text']
	cipher = encode(text)
	return render_template("my-cipher.html", cipher = cipher)

if __name__ == '__main__':
	app.run(debug=True)