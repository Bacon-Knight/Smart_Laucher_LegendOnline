setTimeout(function() {
    var emailInput = document.querySelector('input[type="email"]') || document.querySelector('input[name="email"]') || document.querySelector('input[name="login"]') || document.querySelector('input[name="account"]') || document.querySelector('input[name="username"]') || document.querySelector('input[type="text"]');
    var passInput = document.querySelector('input[type="password"]') || document.querySelector('input[name="password"]');
    
    if(emailInput && passInput) {
        emailInput.value = __EMAIL__;
        passInput.value = __PASSWORD__;
        
        emailInput.dispatchEvent(new Event('input', { bubbles: true }));
        passInput.dispatchEvent(new Event('input', { bubbles: true }));
        emailInput.dispatchEvent(new Event('change', { bubbles: true }));
        passInput.dispatchEvent(new Event('change', { bubbles: true }));
        
        var btn = document.querySelector('button[type="submit"], input[type="submit"], .btn-login, .login-btn, #btnLogin') || document.evaluate("//*[contains(text(), 'Login')]", document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue;
        if(btn && typeof btn.click === 'function') {
            btn.click();
        } else if (emailInput.form) {
            emailInput.form.submit();
        }
        console.log("Credenciais injetadas pelo Custom Launcher!");
    }

    // Auto-clique em botões de entrada/jogo caso esteja na lista de servidores
    setTimeout(function() {
        var playBtn = document.querySelector('.btn-play, .play-btn, .btn-enter, #btnPlay, .enter-game, .btn_start') ||
                      document.evaluate("//a[contains(text(), 'Jogar') or contains(text(), 'Entrar') or contains(text(), 'Play')]", document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue ||
                      document.evaluate("//button[contains(text(), 'Jogar') or contains(text(), 'Entrar') or contains(text(), 'Play')]", document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue;
        if(playBtn && typeof playBtn.click === 'function') {
            playBtn.click();
            console.log("Botão de entrada no jogo clicado automaticamente!");
        }
    }, 1500);
}, 1500);
