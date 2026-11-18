(function () {
  'use strict';
  // ES5 + XMLHttpRequest de propósito: funciona em navegadores de tablets antigos.
  // Sem login neste aparelho: volta para a tela de entrada.
  var USER = null;
  try { USER = JSON.parse(sessionStorage.getItem('almox_user')); } catch (e) {}
  if (!USER) { location.replace('/entrar'); return; }
  var ADMIN = String(USER.sector || '').toLowerCase() === 'admin';
  var KEYS = ['product', 'contributor', 'sector', 'transaction'];
  var S = { product: [], contributor: [], contributorOptions: [], sector: [], transaction: [] };
  var tab = 'product', q = '', hist = 50, acts = [], tt;
  var F = { type: 'saida', prod: '', contr: '', qty: 1, date: today() };
  var R = { start: today(), end: today()}

  function $(id) { return document.getElementById(id); }
  function pad(n) { return n < 10 ? '0' + n : '' + n; }
  function today() { var d = new Date(); return d.getFullYear() + '-' + pad(d.getMonth() + 1) + '-' + pad(d.getDate()); }
  function esc(s) {
    return String(s == null ? '' : s).replace(/[&<>"']/g, function (c) {
      return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c];
    });
  }
  function fmtDate(s) {
    var t = Date.parse(s);
    if (isNaN(t)) return s || '';
    var d = new Date(t);
    return pad(d.getUTCDate()) + '/' + pad(d.getUTCMonth() + 1) + '/' + d.getUTCFullYear();
  }
  function byId(k, id) {
    var a = S[k], i;
    for (i = 0; i < a.length; i++) if (a[i].id == id) return a[i];
    return null;
  }
  function nm(k, id) { var o = byId(k, id); return o ? o.name : '#' + id; }
  function sorted(a) {
    return a.slice().sort(function (x, y) {
      return String(x.name).toLowerCase() < String(y.name).toLowerCase() ? -1 : 1;
    });
  }
  function friendly(m) {
    if (/foreign key/i.test(m)) return 'Não é possível excluir: existem registros vinculados a este item.';
    if (/duplicate key|unique/i.test(m)) return 'Já existe um registro com esse nome.';
    return m;
  }

  // ---------- API ----------
  function api(method, url, body, cb) {
    var x = new XMLHttpRequest(), u = url;
    if (method === 'GET') u += (url.indexOf('?') < 0 ? '?' : '&') + '_=' + new Date().getTime(); // evita cache de WebView antigo
    x.open(method, u, true);
    x.timeout = 15000;
    if (body) x.setRequestHeader('Content-Type', 'application/json');
    x.onreadystatechange = function () {
      if (x.readyState !== 4) return;
      var d = null;
      try { d = JSON.parse(x.responseText); } catch (e) {}
      if (x.status === 401) {
        try { sessionStorage.removeItem('almox_user'); } catch (e2) {}
        location.replace('/entrar');
        return;
      }
      if (x.status >= 200 && x.status < 300) return cb(null, d);
      if (!x.status) return cb(new Error('Sem conexão com o servidor.'));
      cb(new Error(d && d.message ? friendly(d.message) : 'Erro no servidor (' + x.status + ').'));
    };
    x.send(body ? JSON.stringify(body) : null);
  }
  function loadAll(cb) {
    var ks = ADMIN ? KEYS : ['product', 'contributor', 'transaction'], n = ks.length, bad = null;
    ks.forEach(function (k) {
      api('GET', '/' + k, null, function (e, d) {
        if (e) bad = e; else S[k] = (d instanceof Array) ? d : [];
        if (--n === 0) {
    if (bad) toast(bad.message, true);

    if (ADMIN) {
        S.contributorOptions = S.contributor;
        if (cb) cb();
    } else {
        api('GET', '/contributor/options', null, function (e, d) {
            if (e) {
                toast(e.message, true);
                S.contributorOptions = [];
            } else {
                S.contributorOptions = d || [];
            }

            if (cb) cb();
        });
    }
}
      });
    });
  }
  function send(b, m, u, body, ok) {
    b.disabled = true;
    api(m, u, body, function (e) {
      b.disabled = false;
      if (e) return merr(e.message);
      closeModal(); toast(ok); loadAll(render);
    });
  }

  // ---------- UI helpers ----------
  function toast(m, bad) {
    var t = $('toast');
    t.textContent = m; t.className = 'show' + (bad ? ' bad' : '');
    clearTimeout(tt);
    tt = setTimeout(function () { t.className = ''; }, 3500);
  }
  function openModal(title, body, btns) {
    var h = '<div class="sheet"><h2>' + title + '</h2><div id="merr" class="merr"></div>' + body + '<div class="row">', i;
    acts = btns;
    for (i = 0; i < btns.length; i++)
      h += '<button class="' + (btns[i].c || '') + '" data-act="mbtn" data-i="' + i + '">' + btns[i].t + '</button>';
    $('modal').innerHTML = h + '</div></div>';
    $('modal').className = 'show';
    document.body.className = 'lock';
  }
  function closeModal() { $('modal').className = ''; $('modal').innerHTML = ''; document.body.className = ''; }
  function merr(m) { var e = $('merr'); if (!e) return toast(m, true); e.textContent = m; e.style.display = 'block'; }
  function fld(id, label, type, v, extra) {
    return '<label for="' + id + '">' + label + '</label><input id="' + id + '" type="' + type + '" value="' + esc(v) + '" ' + (extra || '') + ' autocomplete="off">';
  }
  function val(id) { return $(id).value.replace(/^\s+|\s+$/g, ''); }
  function opts(a, sel, ph, withStock) {
    var h = '<option value="">' + ph + '</option>', i;
    a = sorted(a);
    for (i = 0; i < a.length; i++)
      h += '<option value="' + a[i].id + '"' + (a[i].id == sel ? ' selected' : '') + '>' + esc(a[i].name) + (withStock ? ' (estoque: ' + a[i].amount + ')' : '') + '</option>';
    return h;
  }
  function confirmDel(txt, method, url) {
    openModal('Confirmar exclusão', '<p>' + txt + '</p>', [
      { t: 'Cancelar' },
      { t: 'Excluir', c: 'danger', f: function (b) { send(b, method, url, null, 'Excluído'); } }
    ]);
  }

  // ---------- Modais de cadastro ----------
  function prodModal(o) {
    var e = !!o, btns = [{ t: 'Cancelar' }];
    if (e) btns.push({ t: 'Excluir', c: 'danger', f: function () {
      confirmDel('Excluir o produto <b>' + esc(o.name) + '</b>?', 'POST', '/delete/product/' + o.id);
    } });
    btns.push({ t: 'Salvar', c: 'pri', f: function (b) {
      var n = val('f_name');
      if (!n) return merr('Informe o nome.');
      if (e) return send(b, 'POST', '/update/product/' + o.id, { name: n, description: val('f_desc'), amount: o.amount }, 'Produto atualizado');
      var a = parseInt(val('f_amt'), 10);
      if (!(a > 0)) return merr('Informe uma quantidade inicial maior que zero.');
      send(b, 'POST', '/product', { name: n, description: val('f_desc'), amount: a }, 'Produto criado');
    } });
    openModal(e ? 'Editar produto' : 'Novo produto',
      fld('f_name', 'Nome', 'text', e ? o.name : '') + fld('f_desc', 'Descrição', 'text', e ? o.description : '') +
      (e ? '<p class="hint">Estoque atual: <b>' + o.amount + '</b>. Para alterar, registre uma entrada ou saída.</p>'
         : fld('f_amt', 'Quantidade inicial', 'number', '', 'inputmode="numeric" pattern="[0-9]*" min="1"')), btns);
  }
  function contrModal() {
    if (!S.sector.length) return toast('Cadastre um setor primeiro.', true);
    openModal('Novo colaborador',
      fld('f_name', 'Nome', 'text', '') + '<label for="f_sec">Setor</label><select id="f_sec">' + opts(S.sector, '', 'Selecione o setor') + '</select>', [
      { t: 'Cancelar' },
      { t: 'Salvar', c: 'pri', f: function (b) {
        var n = val('f_name'), s = $('f_sec').value;
        if (!n) return merr('Informe o nome.');
        if (!s) return merr('Selecione o setor.');
        send(b, 'POST', '/contributor', { name: n, id_sector: parseInt(s, 10) }, 'Colaborador criado');
      } }
    ]);
  }
  function secModal() {
    openModal('Novo setor', fld('f_name', 'Nome', 'text', '') + fld('f_desc', 'Descrição', 'text', ''), [
      { t: 'Cancelar' },
      { t: 'Salvar', c: 'pri', f: function (b) {
        var n = val('f_name');
        if (!n) return merr('Informe o nome.');
        send(b, 'POST', '/sector/create', { name: n, description: val('f_desc') }, 'Setor criado');
      } }
    ]);
  }

  // ---------- Movimentar ----------
  function moveHtml() {
    var h, T = S.transaction.slice().sort(function (a, b) { return b.id - a.id; }), i, t, isIn;
    h = '<div class="panel"><div class="seg">' +
      '<button class="' + (F.type === 'entrada' ? 'in' : '') + '" data-act="type" data-t="entrada">+ Entrada</button>' +
      '<button class="' + (F.type === 'saida' ? 'out' : '') + '" data-act="type" data-t="saida">− Saída</button></div>' +
      '<label for="t_prod">Produto</label><select id="t_prod">' + opts(S.product, F.prod, 'Selecione o produto', true) + '</select>' +
      '<label for="t_contr">Colaborador</label><select id="t_contr">' + opts(S.contributorOptions, F.contr, 'Selecione o colaborador') + '</select>' +
      '<label for="t_qty">Quantidade</label><div class="step"><button data-act="step" data-d="-1">−</button>' +
      '<input id="t_qty" type="number" inputmode="numeric" pattern="[0-9]*" min="1" value="' + esc(F.qty) + '">' +
      '<button data-act="step" data-d="1">+</button></div>' +
      fld('t_date', 'Data', 'date', F.date, 'readonly placeholder="AAAA-MM-DD"') +
      '<button class="go ' + (F.type === 'entrada' ? 'in' : 'out') + '" data-act="doMove">Registrar ' + (F.type === 'entrada' ? 'entrada' : 'saída') + '</button></div>' +
      '<h3>Últimas movimentações</h3><div class="list">';
    for (i = 0; i < T.length && i < hist; i++) {
      t = T[i]; isIn = t.type === 'entrada';
      h += '<div class="card"><div class="grow"><b>' + esc(nm('product', t.id_product)) + '</b><small>' +
        esc(nm('contributor', t.id_contributor)) + ' · ' + fmtDate(t.date_transaction) + '</small></div>' +
        '<span class="tag ' + (isIn ? 'in' : 'out') + '">' + (isIn ? '+' : '−') + t.amount + '</span></div>';
    }
    if (!T.length) h += '<p class="empty">Nenhuma movimentação ainda.</p>';
    if (T.length > hist) h += '<button class="more" data-act="more">Mostrar mais</button>';
    return h + '</div>';
  }
  function doMove(b) {
    var n = parseInt(F.qty, 10);
    if (!F.prod) return toast('Selecione o produto.', true);
    if (!F.contr) return toast('Selecione o colaborador.', true);
    if (!(n > 0)) return toast('Informe uma quantidade maior que zero.', true);
    if (!/^\d{4}-\d{2}-\d{2}$/.test(F.date)) return toast('Data inválida (use AAAA-MM-DD).', true);
    b.disabled = true;
    api('POST', '/transaction/create', { id_product: parseInt(F.prod, 10), id_contributor: parseInt(F.contr, 10), date_transaction: getCurrentDateTime(), amount: n, type: F.type }, function (e) {
      b.disabled = false;
      if (e) return toast(e.message, true);
      toast('Movimentação registrada');
      F.prod = ''; F.qty = 1;
      loadAll(render);
    });
  }
  function syncF(e) {
    var t = e.target;
    if (t.id === 't_prod') F.prod = t.value;
    else if (t.id === 't_contr') F.contr = t.value;
    else if (t.id === 't_qty') F.qty = t.value;
    else if (t.id === 't_date') F.date = t.value;
  }

  // ---------- Listas ----------
  function match(o, fs) {
    if (!q) return true;
    var s = q.toLowerCase(), i;
    for (i = 0; i < fs.length; i++) if (String(o[fs[i]] || '').toLowerCase().indexOf(s) > -1) return true;
    return false;
  }
  function list() {
    var h = '', n = 0, i, o, a;
    if (tab === 'product') {
      a = sorted(S.product);
      for (i = 0; i < a.length; i++) {
        o = a[i]; if (!match(o, ['name', 'description'])) continue; n++;
        h += '<div class="card" data-act="editp" data-id="' + o.id + '"><div class="grow"><b>' + esc(o.name) + '</b><small>' + esc(o.description) + '</small></div>' +
          '<div class="qty' + (o.amount <= 0 ? ' zero' : '') + '">' + o.amount + '</div>' +
          '<div class="acts"><button class="in" data-act="mov" data-t="entrada" data-id="' + o.id + '">+ Entrada</button>' +
          '<button class="out" data-act="mov" data-t="saida" data-id="' + o.id + '">− Saída</button></div></div>';
      }
    } else if (tab === 'contributor') {
      a = sorted(S.contributor);
      for (i = 0; i < a.length; i++) {
        o = a[i]; if (!match(o, ['name'])) continue; n++;
        h += '<div class="card"><div class="grow"><b>' + esc(o.name) + '</b><small>Setor: ' + esc(nm('sector', o.id_sector)) + '</small></div>' +
          '<button class="danger" data-act="delc" data-id="' + o.id + '">Excluir</button></div>';
      }
    } else {
      a = sorted(S.sector);
      for (i = 0; i < a.length; i++) {
        o = a[i]; if (!match(o, ['name', 'description'])) continue; n++;
        h += '<div class="card"><div class="grow"><b>' + esc(o.name) + '</b><small>' + esc(o.description) + '</small></div>' +
          '<button class="danger" data-act="dels" data-id="' + o.id + '">Excluir</button></div>';
      }
    }
    $('list').innerHTML = n ? h : '<p class="empty">Nenhum item encontrado.</p>';
  }

  function reportHtml() {
      return '<div class="panel">' +
          '<h2>Relatório de Almoxarifado</h2>' +

          '<label for="report_start">Data inicial</label>' +
          '<input type="date" id="report_start" value="' + esc(R.start) + '">' +

          '<label for="report_end">Data final</label>' +
          '<input type="date" id="report_end" value="' + esc(R.end) + '">' +

          '<button class="go in" data-act="exportReport">' +
          'Exportar PDF' +
          '</button>' +
          '</div>';
  }

  function render() {
    var v = $('view'), bs = document.querySelectorAll('nav button'), i;
    for (i = 0; i < bs.length; i++) bs[i].className = bs[i].getAttribute('data-t') === tab ? 'on' : '';
    if (tab === 'move') { v.innerHTML = moveHtml(); return; }
    if (tab === 'report') {
    v.innerHTML = reportHtml();
    return;
    }
    v.innerHTML = '<div class="bar"><input id="q" type="search" placeholder="Buscar..." autocomplete="off" value="' + esc(q) + '">' +
      '<button class="pri" data-act="new">+ Novo</button></div><div id="list" class="list"></div>';
    $('q').oninput = function () { q = this.value; list(); };
    list();
  }
  function show(t) { if (!ADMIN && (t === 'contributor' || t === 'sector')) t = 'product'; tab = t; q = ''; hist = 50; render(); $('view').scrollTop = 0; }

  function logout() {
    api('POST', '/logout', null, function () {
      try { sessionStorage.removeItem('almox_user'); } catch (e) {}
      location.replace('/entrar');
    });
  }

  // ---------- Eventos (um único listener, ideal para touch) ----------
  document.addEventListener('click', function (e) {
    var el = e.target, a, id, t, o;
    while (el && el.getAttribute && !(a = el.getAttribute('data-act'))) el = el.parentNode;
    if (!a) { if (e.target === $('modal')) closeModal(); return; }
    id = el.getAttribute('data-id'); t = el.getAttribute('data-t');
    if (a === 'tab') show(t);
    else if (a === 'refresh') loadAll(function () { render(); toast('Atualizado'); });
    else if (a === 'new') { if (tab === 'product') prodModal(); else if (tab === 'contributor') contrModal(); else secModal(); }
    else if (a === 'editp') { o = byId('product', id); if (o) prodModal(o); }
    else if (a === 'mov') { F.type = t; F.prod = id; F.qty = 1; show('move'); }
    else if (a === 'delc') { o = byId('contributor', id); confirmDel('Excluir o colaborador <b>' + esc(o ? o.name : id) + '</b>?', 'DELETE', '/contributor/delete/' + id); }
    else if (a === 'dels') { o = byId('sector', id); confirmDel('Excluir o setor <b>' + esc(o ? o.name : id) + '</b>?', 'DELETE', '/sector/delete/' + id); }
    else if (a === 'type') { F.type = t; render(); }
    else if (a === 'step') { F.qty = Math.max(1, (parseInt($('t_qty').value, 10) || 0) + parseInt(el.getAttribute('data-d'), 10)); $('t_qty').value = F.qty; }
    else if (a === 'logout') logout();
    else if (a === 'doMove') doMove(el);
    else if (a === 'more') { hist += 50; render(); }
    else if (a === 'mbtn') { o = acts[parseInt(el.getAttribute('data-i'), 10)]; if (o.f) o.f(el); else closeModal(); }
    else if (a === 'exportReport') {
    var start = $('report_start').value;
    var end = $('report_end').value;

    if (!start || !end) {
        return toast('Informe as duas datas.', true);
    }

    if (start > end) {
        return toast('A data inicial não pode ser maior que a final.', true);
    }

    window.location.href =
        '/report/pdf?start_date=' +
        encodeURIComponent(start) +
        '&end_date=' +
        encodeURIComponent(end);
  }
  });
  $('view').addEventListener('change', syncF);
  $('view').addEventListener('input', syncF);

  $('who').textContent = USER.name + (ADMIN ? ' (admin)' : '');
  if (!ADMIN) { // colaboradores e setores: só admin
    var nb = document.querySelectorAll('nav button'), k2, tn;
    for (k2 = 0; k2 < nb.length; k2++) {
      tn = nb[k2].getAttribute('data-t');
      if (tn === 'contributor' || tn === 'sector') nb[k2].style.display = 'none';
    }
  }
  $('view').innerHTML = '<p class="empty">Carregando...</p>';
  loadAll(render);
})();

function getCurrentDateTime() {
  var now = new Date();

  var pad = function (n) {
    return n < 10 ? '0' + n : n;
  };

  return now.getFullYear() + '-' +
    pad(now.getMonth() + 1) + '-' +
    pad(now.getDate()) + 'T' +
    pad(now.getHours()) + ':' +
    pad(now.getMinutes()) + ':' +
    pad(now.getSeconds());
}
