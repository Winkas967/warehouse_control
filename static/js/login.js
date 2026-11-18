(function () {
  'use strict';
  // ES5 + XMLHttpRequest de propósito: funciona em navegadores de tablets antigos.
  var KEY = 'almox_user';
  function $(id) { return document.getElementById(id); }

  // Já logado neste aparelho? Vai direto para o sistema.
  try { if (sessionStorage.getItem(KEY)) { location.replace('/'); return; } } catch (e) {}

  function showErr(m) { var e = $('err'); e.textContent = m; e.style.display = 'block'; }
  function clearErr() { $('err').style.display = 'none'; }

  // O back devolve HTTP 200 mesmo no erro ({"message": ...}); o sucesso é {id, name, id_sector}.
  function msgFrom(d) {
    var m = d && d.message ? String(d.message) : '';
    if (!m || /NoneType|mapping|argument after/i.test(m)) return 'Nome ou senha incorretos.';
    return m;
  }

  function login(name, password, cb) {
    var x = new XMLHttpRequest();
    x.open('POST', '/login', true);
    x.timeout = 15000;
    x.setRequestHeader('Content-Type', 'application/json');
    x.onreadystatechange = function () {
      if (x.readyState !== 4) return;
      var d = null;
      try { d = JSON.parse(x.responseText); } catch (e) {}
      if (!x.status) return cb('Sem conexão com o servidor.');
      if (x.status >= 200 && x.status < 300 && d && d.id != null) return cb(null, d);
      cb(msgFrom(d));
    };
    x.send(JSON.stringify({ name: name, password: password }));
  }

  $('f').addEventListener('submit', function (e) {
    e.preventDefault();
    var name = $('name').value.replace(/^\s+|\s+$/g, ''), pw = $('password').value, b = $('go');
    clearErr();
    if (!name) return showErr('Informe o nome.');
    if (!pw) return showErr('Informe a senha.');
    b.disabled = true; b.textContent = 'Entrando...';
    login(name, pw, function (err, user) {
      b.disabled = false; b.textContent = 'Entrar';
      if (err) { $('password').value = ''; return showErr(err); }
      try { sessionStorage.setItem(KEY, JSON.stringify(user)); } catch (e2) {}
      location.replace('/');
    });
  });

  // Mostrar/ocultar senha
  $('eye').addEventListener('click', function () {
    var p = $('password'), show = p.type === 'password';
    p.type = show ? 'text' : 'password';
    this.textContent = show ? 'Ocultar' : 'Mostrar';
  });
})();
