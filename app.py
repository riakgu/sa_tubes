from flask import Flask, render_template, request
import datetime

app = Flask(__name__)

def lcs_bf(X, Y, m, n):
    if m == 0 or n == 0:
        return 0
    if X[m-1] == Y[n-1]:
        return 1 + lcs_bf(X, Y, m - 1, n - 1)
    else:
        return max(lcs_bf(X, Y, m, n -1), lcs_bf(X, Y, m - 1, n))

def lcs_dp(X, Y, m, n):
    LCS = [[0] * (n+1) for _ in range(m + 1)]

    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if X[i - 1] == Y[j- 1]:
                LCS[i][j] = 1 + LCS[i - 1][j - 1]
            else:
                LCS[i][j] = max(LCS[i - 1][j], LCS[i][j - 1])

    return LCS[m][n]

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/result', methods=['POST'])
def result():
    text1 = request.form['text1'].lower().split()
    text2 = request.form['text2'].lower().split()

    algorithm = request.form.get('algorithm')

    start_time = datetime.datetime.now()

    if algorithm == 'bf':
        lcs_length = lcs_bf(text1, text2, len(text1), len(text2))
    else:
        lcs_length = lcs_dp(text1, text2, len(text1), len(text2))

    end_time = datetime.datetime.now()
    running_time = end_time - start_time
    similarity = (lcs_length / max(len(text1), len(text2))) * 100

    return render_template('result.html', 
                           lcs_length=lcs_length, 
                           running_time=running_time.total_seconds(), 
                           similarity=similarity, 
                           algorithm=algorithm)

if __name__ == '__main__':
    app.run()
