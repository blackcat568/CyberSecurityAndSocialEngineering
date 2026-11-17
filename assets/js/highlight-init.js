// Регистрация языков и инициализация highlight.js
document.addEventListener('DOMContentLoaded', () => {
    if (typeof hljs === 'undefined') return;

    // --- Регистрация nftables ---
    hljs.registerLanguage('nftables', (hljs) => {
        return {
            name: 'nftables',
            aliases: ['nft'],
            keywords: 'table chain type hook priority policy accept drop reject log counter ip ip6 inet ether tcp udp icmp ct state established related new invalid dport sport saddr daddr',
            contains: [
                hljs.HASH_COMMENT_MODE,
                hljs.QUOTE_STRING_MODE,
                hljs.NUMBER_MODE,
                { className: 'meta', begin: 'include\\b', end: '$' }
            ]
        };
    });

    // --- Регистрация bash ---
    hljs.registerLanguage('bash', function(hljs) {
        return {
            name: 'bash',
            aliases: ['sh'],
            keywords: {
                keyword: 'if then else fi for while do done case esac function select',
                built_in: 'sudo echo cat grep sort uniq dig curl wget nft systemctl journalctl ls cd pwd mkdir rm cp mv chmod chown kill pkill top htop ps netstat ss ip ifconfig',
                literal: 'true false'
            },
            contains: [
                hljs.HASH_COMMENT_MODE,
                { className: 'string', begin: /"/, end: /"/, contains: [hljs.BACKSLASH_ESCAPE] },
                { className: 'string', begin: /'/, end: /'/ },
                { className: 'variable', begin: /\$[a-zA-Z_][a-zA-Z0-9_]*/ },
                { className: 'meta', begin: '#!', end: '$' }
            ]
        };
    });

    // --- Регистрация sysctl ---
    hljs.registerLanguage('sysctl', (hljs) => {
        return {
            name: 'sysctl',
            contains: [
                hljs.HASH_COMMENT_MODE,
                hljs.NUMBER_MODE,
                { className: 'attr', begin: /^[a-zA-Z0-9_\.\-\*]+/ },
                { className: 'string', begin: /(?<==\s*)[a-zA-Z_/]+/ }
            ]
        };
    });

    // --- Инициализация подсветки ---
    function initHighlighting() {
        document.querySelectorAll('code[data-highlighted]').forEach(el => {
            delete el.dataset.highlighted;
        });
        hljs.highlightAll();
    }

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', initHighlighting);
    } else {
        initHighlighting();
    }
});
