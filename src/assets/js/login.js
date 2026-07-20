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
}, 1500);
