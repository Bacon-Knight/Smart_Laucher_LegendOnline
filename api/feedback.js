// api/feedback.js
// Serverless Gateway da Vercel para envio seguro de feedback ao Discord
// Mantém a URL do Webhook escondida nas Variáveis de Ambiente do painel Vercel.

export default async function handler(req, res) {
    // Configura cabeçalhos de CORS (para permitir chamadas do Launcher)
    res.setHeader('Access-Control-Allow-Origin', '*');
    res.setHeader('Access-Control-Allow-Methods', 'POST, OPTIONS');
    res.setHeader('Access-Control-Allow-Headers', 'Content-Type, X-App-Secret');

    if (req.method === 'OPTIONS') {
        return res.status(200).end();
    }

    if (req.method === 'GET') {
        return res.status(200).json({
            status: 'online',
            service: 'BK Launcher Discord Feedback Gateway',
            version: 'v2.4.2',
            message: 'Gateway de feedback funcionando perfeitamente. Use POST para enviar relatórios.'
        });
    }

    if (req.method !== 'POST') {
        return res.status(405).json({ error: 'Método não permitido. Use POST.' });
    }

    // Validação de segurança via Secret Header (evita uso não autorizado por terceiros)
    const appSecret = process.env.APP_CLIENT_SECRET;
    if (appSecret) {
        const reqSecret = req.headers['x-app-secret'];
        if (!reqSecret || reqSecret !== appSecret) {
            return res.status(401).json({ error: 'Acesso não autorizado ao gateway.' });
        }
    }

    const webhookUrl = process.env.DISCORD_WEBHOOK_URL;
    if (!webhookUrl) {
        return res.status(500).json({ error: 'DISCORD_WEBHOOK_URL não configurada no painel Vercel' });
    }

    try {
        const body = typeof req.body === 'string' ? JSON.parse(req.body) : req.body;
        const { category, message, user_contact, include_logs, log_snippet } = body || {};

        if (!message || message.trim() === '') {
            return res.status(400).json({ error: 'Mensagem não pode ser vazia' });
        }

        const categoryStr = (category || 'GERAL').toUpperCase();
        const isBug = (category || '').toLowerCase().includes('bug');

        const embed = {
            title: `🥓 Novo Feedback do Launcher [${categoryStr}]`,
            color: isBug ? 13214788 : 3487635,
            fields: [
                { name: '📁 Categoria', value: category || 'Geral', inline: true },
                { name: '👤 Contato', value: user_contact || 'Anônimo', inline: true },
                { name: '💬 Mensagem / Relatório', value: message.slice(0, 1024) }
            ],
            footer: { text: 'BK Launcher LO • Vercel Secure Gateway v2.4.2' },
            timestamp: new Date().toISOString()
        };

        if (include_logs && log_snippet && log_snippet.trim() !== '') {
            embed.fields.push({
                name: '📋 Últimas Linhas do Log',
                value: `\`\`\`text\n${log_snippet.slice(0, 950)}\n\`\`\``,
                inline: false
            });
        }

        const discordPayload = {
            username: 'Bacon Knight Bot',
            avatar_url: 'https://raw.githubusercontent.com/Bacon-Knight/Smart_Laucher_LegendOnline/main/bacon_knight.ico',
            embeds: [embed]
        };

        const response = await fetch(webhookUrl, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(discordPayload)
        });

        if (response.ok || response.status === 204) {
            return res.status(200).json({ success: true });
        } else {
            const errText = await response.text();
            return res.status(500).json({ error: `Discord recusou: ${errText}` });
        }
    } catch (err) {
        return res.status(500).json({ error: `Erro no servidor: ${err.message}` });
    }
}
