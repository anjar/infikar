"""
Username validation rules and reserved words
"""

# Reserved usernames that cannot be used
RESERVED_USERNAMES = {
    # Admin and system accounts
    'admin', 'administrator', 'root', 'system', 'support', 'help', 'info',
    'contact', 'about', 'privacy', 'terms', 'legal', 'security', 'staff',
    
    # Platform-specific
    'api', 'app', 'www', 'mail', 'email', 'ftp', 'blog', 'news',
    'forum', 'community', 'chat', 'support', 'helpdesk', 'billing', 'payment',
    'account', 'accounts', 'user', 'users', 'member', 'members', 'profile',
    'profiles', 'dashboard', 'settings', 'preferences', 'config', 'configuration',
    
    # Common web terms
    'home', 'index', 'main', 'default', 'test', 'demo', 'sample', 'example',
    'welcome', 'hello', 'hi', 'hey', 'wow', 'cool', 'awesome', 'amazing',
    'great', 'good', 'bad', 'best', 'worst', 'new', 'old', 'latest', 'popular',
    
    # Social media and communication
    'social', 'media', 'facebook', 'twitter', 'instagram', 'linkedin', 'youtube',
    'tiktok', 'snapchat', 'discord', 'telegram', 'whatsapp', 'messenger',
    'chat', 'message', 'messages', 'notification', 'notifications', 'alert',
    'alerts', 'reminder', 'reminders', 'invite', 'invitation', 'invitations',
    
    # Business and commerce
    'business', 'company', 'corp', 'corporation', 'inc', 'llc', 'ltd', 'limited',
    'shop', 'store', 'market', 'marketplace', 'commerce', 'ecommerce', 'sell',
    'buy', 'purchase', 'order', 'orders', 'cart', 'checkout', 'payment',
    'billing', 'invoice', 'receipt', 'refund', 'return', 'shipping', 'delivery',
    
    # Technical terms
    'server', 'host', 'hosting', 'domain', 'subdomain', 'dns', 'ssl', 'https',
    'http', 'www', 'ftp', 'sftp', 'ssh', 'database', 'db', 'sql', 'mysql',
    'postgresql', 'mongodb', 'redis', 'cache', 'cdn', 'cdn', 'aws', 'azure',
    'google', 'microsoft', 'apple', 'amazon', 'netflix', 'spotify', 'youtube',
    
    # Common words that might cause confusion
    'null', 'undefined', 'none', 'empty', 'blank', 'space', 'spaces', 'tab',
    'newline', 'return', 'enter', 'backspace', 'delete', 'remove', 'clear',
    'reset', 'refresh', 'reload', 'restart', 'start', 'stop', 'pause', 'play',
    'next', 'previous', 'back', 'forward', 'up', 'down', 'left', 'right',
    'top', 'bottom', 'center', 'middle', 'side', 'corner', 'edge', 'border',
    
    # Inappropriate content (basic list)
    'fuck', 'shit', 'bitch', 'ass', 'asshole', 'damn', 'hell', 'crap',
    'stupid', 'idiot', 'moron', 'dumb', 'retard', 'gay', 'lesbian', 'fag',
    'nigger', 'nigga', 'chink', 'kike', 'spic', 'wetback', 'towelhead',
    'terrorist', 'bomb', 'kill', 'murder', 'death', 'die', 'suicide',
    'rape', 'sex', 'porn', 'pornography', 'nude', 'naked', 'nude', 'naked',
    'drug', 'drugs', 'cocaine', 'heroin', 'marijuana', 'weed', 'alcohol',
    'drunk', 'drinking', 'smoking', 'cigarette', 'cigar', 'pipe', 'bong',
    
    # Common names that might be problematic
    'jesus', 'christ', 'god', 'allah', 'buddha', 'mohammed', 'muhammad',
    'hitler', 'stalin', 'mussolini', 'mao', 'lenin', 'putin', 'trump',
    'biden', 'obama', 'bush', 'clinton', 'reagan', 'nixon', 'kennedy',
    
    # Numbers and special characters
    '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12',
    '13', '14', '15', '16', '17', '18', '19', '20', '21', '22', '23',
    '24', '25', '26', '27', '28', '29', '30', '31', '32', '33', '34',
    '35', '36', '37', '38', '39', '40', '41', '42', '43', '44', '45',
    '46', '47', '48', '49', '50', '51', '52', '53', '54', '55', '56',
    '57', '58', '59', '60', '61', '62', '63', '64', '65', '66', '67',
    '68', '69', '70', '71', '72', '73', '74', '75', '76', '77', '78',
    '79', '80', '81', '82', '83', '84', '85', '86', '87', '88', '89',
    '90', '91', '92', '93', '94', '95', '96', '97', '98', '99', '100',
    
    # Common single characters and short words
    'a', 'an', 'as', 'at', 'be', 'by', 'do', 'go', 'he', 'if', 'in', 'is',
    'it', 'me', 'my', 'no', 'of', 'on', 'or', 'so', 'to', 'up', 'us', 'we',
    'am', 'are', 'was', 'were', 'been', 'being', 'have', 'has', 'had',
    'having', 'will', 'would', 'could', 'should', 'may', 'might', 'must',
    'can', 'cannot', 'cant', 'wont', 'dont', 'doesnt', 'didnt', 'havent',
    'hasnt', 'hadnt', 'isnt', 'arent', 'wasnt', 'werent', 'wont', 'wouldnt',
    'couldnt', 'shouldnt', 'mustnt', 'neednt', 'oughtnt', 'darent', 'usednt',
    
    # Common abbreviations
    'ab', 'ac', 'ad', 'ae', 'af', 'ag', 'ah', 'ai', 'aj', 'ak', 'al', 'am',
    'an', 'ao', 'ap', 'aq', 'ar', 'as', 'at', 'au', 'av', 'aw', 'ax', 'ay',
    'az', 'ba', 'bb', 'bc', 'bd', 'be', 'bf', 'bg', 'bh', 'bi', 'bj', 'bk',
    'bl', 'bm', 'bn', 'bo', 'bp', 'bq', 'br', 'bs', 'bt', 'bu', 'bv', 'bw',
    'bx', 'by', 'bz', 'ca', 'cb', 'cc', 'cd', 'ce', 'cf', 'cg', 'ch', 'ci',
    'cj', 'ck', 'cl', 'cm', 'cn', 'co', 'cp', 'cq', 'cr', 'cs', 'ct', 'cu',
    'cv', 'cw', 'cx', 'cy', 'cz', 'da', 'db', 'dc', 'dd', 'de', 'df', 'dg',
    'dh', 'di', 'dj', 'dk', 'dl', 'dm', 'dn', 'do', 'dp', 'dq', 'dr', 'ds',
    'dt', 'du', 'dv', 'dw', 'dx', 'dy', 'dz', 'ea', 'eb', 'ec', 'ed', 'ee',
    'ef', 'eg', 'eh', 'ei', 'ej', 'ek', 'el', 'em', 'en', 'eo', 'ep', 'eq',
    'er', 'es', 'et', 'eu', 'ev', 'ew', 'ex', 'ey', 'ez', 'fa', 'fb', 'fc',
    'fd', 'fe', 'ff', 'fg', 'fh', 'fi', 'fj', 'fk', 'fl', 'fm', 'fn', 'fo',
    'fp', 'fq', 'fr', 'fs', 'ft', 'fu', 'fv', 'fw', 'fx', 'fy', 'fz', 'ga',
    'gb', 'gc', 'gd', 'ge', 'gf', 'gg', 'gh', 'gi', 'gj', 'gk', 'gl', 'gm',
    'gn', 'go', 'gp', 'gq', 'gr', 'gs', 'gt', 'gu', 'gv', 'gw', 'gx', 'gy',
    'gz', 'ha', 'hb', 'hc', 'hd', 'he', 'hf', 'hg', 'hh', 'hi', 'hj', 'hk',
    'hl', 'hm', 'hn', 'ho', 'hp', 'hq', 'hr', 'hs', 'ht', 'hu', 'hv', 'hw',
    'hx', 'hy', 'hz', 'ia', 'ib', 'ic', 'id', 'ie', 'if', 'ig', 'ih', 'ii',
    'ij', 'ik', 'il', 'im', 'in', 'io', 'ip', 'iq', 'ir', 'is', 'it', 'iu',
    'iv', 'iw', 'ix', 'iy', 'iz', 'ja', 'jb', 'jc', 'jd', 'je', 'jf', 'jg',
    'jh', 'ji', 'jj', 'jk', 'jl', 'jm', 'jn', 'jo', 'jp', 'jq', 'jr', 'js',
    'jt', 'ju', 'jv', 'jw', 'jx', 'jy', 'jz', 'ka', 'kb', 'kc', 'kd', 'ke',
    'kf', 'kg', 'kh', 'ki', 'kj', 'kk', 'kl', 'km', 'kn', 'ko', 'kp', 'kq',
    'kr', 'ks', 'kt', 'ku', 'kv', 'kw', 'kx', 'ky', 'kz', 'la', 'lb', 'lc',
    'ld', 'le', 'lf', 'lg', 'lh', 'li', 'lj', 'lk', 'll', 'lm', 'ln', 'lo',
    'lp', 'lq', 'lr', 'ls', 'lt', 'lu', 'lv', 'lw', 'lx', 'ly', 'lz', 'ma',
    'mb', 'mc', 'md', 'me', 'mf', 'mg', 'mh', 'mi', 'mj', 'mk', 'ml', 'mm',
    'mn', 'mo', 'mp', 'mq', 'mr', 'ms', 'mt', 'mu', 'mv', 'mw', 'mx', 'my',
    'mz', 'na', 'nb', 'nc', 'nd', 'ne', 'nf', 'ng', 'nh', 'ni', 'nj', 'nk',
    'nl', 'nm', 'nn', 'no', 'np', 'nq', 'nr', 'ns', 'nt', 'nu', 'nv', 'nw',
    'nx', 'ny', 'nz', 'oa', 'ob', 'oc', 'od', 'oe', 'of', 'og', 'oh', 'oi',
    'oj', 'ok', 'ol', 'om', 'on', 'oo', 'op', 'oq', 'or', 'os', 'ot', 'ou',
    'ov', 'ow', 'ox', 'oy', 'oz', 'pa', 'pb', 'pc', 'pd', 'pe', 'pf', 'pg',
    'ph', 'pi', 'pj', 'pk', 'pl', 'pm', 'pn', 'po', 'pp', 'pq', 'pr', 'ps',
    'pt', 'pu', 'pv', 'pw', 'px', 'py', 'pz', 'qa', 'qb', 'qc', 'qd', 'qe',
    'qf', 'qg', 'qh', 'qi', 'qj', 'qk', 'ql', 'qm', 'qn', 'qo', 'qp', 'qq',
    'qr', 'qs', 'qt', 'qu', 'qv', 'qw', 'qx', 'qy', 'qz', 'ra', 'rb', 'rc',
    'rd', 're', 'rf', 'rg', 'rh', 'ri', 'rj', 'rk', 'rl', 'rm', 'rn', 'ro',
    'rp', 'rq', 'rr', 'rs', 'rt', 'ru', 'rv', 'rw', 'rx', 'ry', 'rz', 'sa',
    'sb', 'sc', 'sd', 'se', 'sf', 'sg', 'sh', 'si', 'sj', 'sk', 'sl', 'sm',
    'sn', 'so', 'sp', 'sq', 'sr', 'ss', 'st', 'su', 'sv', 'sw', 'sx', 'sy',
    'sz', 'ta', 'tb', 'tc', 'td', 'te', 'tf', 'tg', 'th', 'ti', 'tj', 'tk',
    'tl', 'tm', 'tn', 'to', 'tp', 'tq', 'tr', 'ts', 'tt', 'tu', 'tv', 'tw',
    'tx', 'ty', 'tz', 'ua', 'ub', 'uc', 'ud', 'ue', 'uf', 'ug', 'uh', 'ui',
    'uj', 'uk', 'ul', 'um', 'un', 'uo', 'up', 'uq', 'ur', 'us', 'ut', 'uu',
    'uv', 'uw', 'ux', 'uy', 'uz', 'va', 'vb', 'vc', 'vd', 've', 'vf', 'vg',
    'vh', 'vi', 'vj', 'vk', 'vl', 'vm', 'vn', 'vo', 'vp', 'vq', 'vr', 'vs',
    'vt', 'vu', 'vv', 'vw', 'vx', 'vy', 'vz', 'wa', 'wb', 'wc', 'wd', 'we',
    'wf', 'wg', 'wh', 'wi', 'wj', 'wk', 'wl', 'wm', 'wn', 'wo', 'wp', 'wq',
    'wr', 'ws', 'wt', 'wu', 'wv', 'ww', 'wx', 'wy', 'wz', 'xa', 'xb', 'xc',
    'xd', 'xe', 'xf', 'xg', 'xh', 'xi', 'xj', 'xk', 'xl', 'xm', 'xn', 'xo',
    'xp', 'xq', 'xr', 'xs', 'xt', 'xu', 'xv', 'xw', 'xx', 'xy', 'xz', 'ya',
    'yb', 'yc', 'yd', 'ye', 'yf', 'yg', 'yh', 'yi', 'yj', 'yk', 'yl', 'ym',
    'yn', 'yo', 'yp', 'yq', 'yr', 'ys', 'yt', 'yu', 'yv', 'yw', 'yx', 'yy',
    'yz', 'za', 'zb', 'zc', 'zd', 'ze', 'zf', 'zg', 'zh', 'zi', 'zj', 'zk',
    'zl', 'zm', 'zn', 'zo', 'zp', 'zq', 'zr', 'zs', 'zt', 'zu', 'zv', 'zw',
    'zx', 'zy', 'zz',
    
    # Bahasa Indonesia reserved words
    # Admin dan sistem
    'admin', 'administrator', 'root', 'sistem', 'dukungan', 'bantuan', 'info',
    'kontak', 'tentang', 'privasi', 'syarat', 'hukum', 'keamanan', 'staf',
    
    # Platform khusus
    'infikar', 'api', 'aplikasi', 'www', 'surat', 'email', 'ftp', 'blog', 'berita',
    'forum', 'komunitas', 'obrolan', 'dukungan', 'layanan', 'pembayaran',
    'akun', 'pengguna', 'anggota', 'profil', 'dashboard', 'pengaturan', 'preferensi',
    'konfigurasi', 'pengaturan',
    
    # Istilah web umum
    'beranda', 'indeks', 'utama', 'default', 'tes', 'demo', 'sampel', 'contoh',
    'selamat', 'datang', 'halo', 'hai', 'he', 'wow', 'keren', 'menakjubkan',
    'bagus', 'baik', 'buruk', 'terbaik', 'terburuk', 'baru', 'lama', 'terbaru', 'populer',
    
    # Media sosial dan komunikasi
    'sosial', 'media', 'facebook', 'twitter', 'instagram', 'linkedin', 'youtube',
    'tiktok', 'snapchat', 'discord', 'telegram', 'whatsapp', 'messenger',
    'obrolan', 'pesan', 'pesan', 'notifikasi', 'peringatan', 'pengingat',
    'undangan', 'undangan',
    
    # Bisnis dan perdagangan
    'bisnis', 'perusahaan', 'korporasi', 'toko', 'toko', 'pasar', 'marketplace',
    'perdagangan', 'ecommerce', 'jual', 'beli', 'pembelian', 'pesanan', 'keranjang',
    'checkout', 'pembayaran', 'penagihan', 'faktur', 'tanda', 'terima', 'pengembalian',
    'pengiriman', 'pengiriman',
    
    # Istilah teknis
    'server', 'host', 'hosting', 'domain', 'subdomain', 'dns', 'ssl', 'https',
    'http', 'www', 'ftp', 'sftp', 'ssh', 'database', 'db', 'sql', 'mysql',
    'postgresql', 'mongodb', 'redis', 'cache', 'cdn', 'aws', 'azure',
    'google', 'microsoft', 'apple', 'amazon', 'netflix', 'spotify', 'youtube',
    
    # Kata-kata umum yang mungkin membingungkan
    'null', 'undefined', 'none', 'kosong', 'blank', 'spasi', 'tab',
    'newline', 'return', 'enter', 'backspace', 'hapus', 'hapus', 'bersih',
    'reset', 'refresh', 'reload', 'restart', 'mulai', 'berhenti', 'jeda', 'main',
    'berikutnya', 'sebelumnya', 'kembali', 'maju', 'atas', 'bawah', 'kiri', 'kanan',
    'atas', 'bawah', 'tengah', 'samping', 'sudut', 'tepi', 'batas',
    
    # Konten tidak pantas (daftar dasar)
    'fuck', 'shit', 'bitch', 'ass', 'asshole', 'damn', 'hell', 'crap',
    'stupid', 'idiot', 'moron', 'dumb', 'retard', 'gay', 'lesbian', 'fag',
    'nigger', 'nigga', 'chink', 'kike', 'spic', 'wetback', 'towelhead',
    'terrorist', 'bomb', 'kill', 'murder', 'death', 'die', 'suicide',
    'rape', 'sex', 'porn', 'pornography', 'nude', 'naked', 'nude', 'naked',
    'drug', 'drugs', 'cocaine', 'heroin', 'marijuana', 'weed', 'alcohol',
    'drunk', 'drinking', 'smoking', 'cigarette', 'cigar', 'pipe', 'bong',
    
    # Nama umum yang mungkin bermasalah
    'jesus', 'christ', 'god', 'allah', 'buddha', 'mohammed', 'muhammad',
    'hitler', 'stalin', 'mussolini', 'mao', 'lenin', 'putin', 'trump',
    'biden', 'obama', 'bush', 'clinton', 'reagan', 'nixon', 'kennedy',
    
    # Angka dan karakter khusus
    '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12',
    '13', '14', '15', '16', '17', '18', '19', '20', '21', '22', '23',
    '24', '25', '26', '27', '28', '29', '30', '31', '32', '33', '34',
    '35', '36', '37', '38', '39', '40', '41', '42', '43', '44', '45',
    '46', '47', '48', '49', '50', '51', '52', '53', '54', '55', '56',
    '57', '58', '59', '60', '61', '62', '63', '64', '65', '66', '67',
    '68', '69', '70', '71', '72', '73', '74', '75', '76', '77', '78',
    '79', '80', '81', '82', '83', '84', '85', '86', '87', '88', '89',
    '90', '91', '92', '93', '94', '95', '96', '97', '98', '99', '100',
    
    # Karakter tunggal dan kata pendek umum
    'a', 'an', 'as', 'at', 'be', 'by', 'do', 'go', 'he', 'if', 'in', 'is',
    'it', 'me', 'my', 'no', 'of', 'on', 'or', 'so', 'to', 'up', 'us', 'we',
    'am', 'are', 'was', 'were', 'been', 'being', 'have', 'has', 'had',
    'having', 'will', 'would', 'could', 'should', 'may', 'might', 'must',
    'can', 'cannot', 'cant', 'wont', 'dont', 'doesnt', 'didnt', 'havent',
    'hasnt', 'hadnt', 'isnt', 'arent', 'wasnt', 'werent', 'wont', 'wouldnt',
    'couldnt', 'shouldnt', 'mustnt', 'neednt', 'oughtnt', 'darent', 'usednt',
    
    # Singkatan umum
    'ab', 'ac', 'ad', 'ae', 'af', 'ag', 'ah', 'ai', 'aj', 'ak', 'al', 'am',
    'an', 'ao', 'ap', 'aq', 'ar', 'as', 'at', 'au', 'av', 'aw', 'ax', 'ay',
    'az', 'ba', 'bb', 'bc', 'bd', 'be', 'bf', 'bg', 'bh', 'bi', 'bj', 'bk',
    'bl', 'bm', 'bn', 'bo', 'bp', 'bq', 'br', 'bs', 'bt', 'bu', 'bv', 'bw',
    'bx', 'by', 'bz', 'ca', 'cb', 'cc', 'cd', 'ce', 'cf', 'cg', 'ch', 'ci',
    'cj', 'ck', 'cl', 'cm', 'cn', 'co', 'cp', 'cq', 'cr', 'cs', 'ct', 'cu',
    'cv', 'cw', 'cx', 'cy', 'cz', 'da', 'db', 'dc', 'dd', 'de', 'df', 'dg',
    'dh', 'di', 'dj', 'dk', 'dl', 'dm', 'dn', 'do', 'dp', 'dq', 'dr', 'ds',
    'dt', 'du', 'dv', 'dw', 'dx', 'dy', 'dz', 'ea', 'eb', 'ec', 'ed', 'ee',
    'ef', 'eg', 'eh', 'ei', 'ej', 'ek', 'el', 'em', 'en', 'eo', 'ep', 'eq',
    'er', 'es', 'et', 'eu', 'ev', 'ew', 'ex', 'ey', 'ez', 'fa', 'fb', 'fc',
    'fd', 'fe', 'ff', 'fg', 'fh', 'fi', 'fj', 'fk', 'fl', 'fm', 'fn', 'fo',
    'fp', 'fq', 'fr', 'fs', 'ft', 'fu', 'fv', 'fw', 'fx', 'fy', 'fz', 'ga',
    'gb', 'gc', 'gd', 'ge', 'gf', 'gg', 'gh', 'gi', 'gj', 'gk', 'gl', 'gm',
    'gn', 'go', 'gp', 'gq', 'gr', 'gs', 'gt', 'gu', 'gv', 'gw', 'gx', 'gy',
    'gz', 'ha', 'hb', 'hc', 'hd', 'he', 'hf', 'hg', 'hh', 'hi', 'hj', 'hk',
    'hl', 'hm', 'hn', 'ho', 'hp', 'hq', 'hr', 'hs', 'ht', 'hu', 'hv', 'hw',
    'hx', 'hy', 'hz', 'ia', 'ib', 'ic', 'id', 'ie', 'if', 'ig', 'ih', 'ii',
    'ij', 'ik', 'il', 'im', 'in', 'io', 'ip', 'iq', 'ir', 'is', 'it', 'iu',
    'iv', 'iw', 'ix', 'iy', 'iz', 'ja', 'jb', 'jc', 'jd', 'je', 'jf', 'jg',
    'jh', 'ji', 'jj', 'jk', 'jl', 'jm', 'jn', 'jo', 'jp', 'jq', 'jr', 'js',
    'jt', 'ju', 'jv', 'jw', 'jx', 'jy', 'jz', 'ka', 'kb', 'kc', 'kd', 'ke',
    'kf', 'kg', 'kh', 'ki', 'kj', 'kk', 'kl', 'km', 'kn', 'ko', 'kp', 'kq',
    'kr', 'ks', 'kt', 'ku', 'kv', 'kw', 'kx', 'ky', 'kz', 'la', 'lb', 'lc',
    'ld', 'le', 'lf', 'lg', 'lh', 'li', 'lj', 'lk', 'll', 'lm', 'ln', 'lo',
    'lp', 'lq', 'lr', 'ls', 'lt', 'lu', 'lv', 'lw', 'lx', 'ly', 'lz', 'ma',
    'mb', 'mc', 'md', 'me', 'mf', 'mg', 'mh', 'mi', 'mj', 'mk', 'ml', 'mm',
    'mn', 'mo', 'mp', 'mq', 'mr', 'ms', 'mt', 'mu', 'mv', 'mw', 'mx', 'my',
    'mz', 'na', 'nb', 'nc', 'nd', 'ne', 'nf', 'ng', 'nh', 'ni', 'nj', 'nk',
    'nl', 'nm', 'nn', 'no', 'np', 'nq', 'nr', 'ns', 'nt', 'nu', 'nv', 'nw',
    'nx', 'ny', 'nz', 'oa', 'ob', 'oc', 'od', 'oe', 'of', 'og', 'oh', 'oi',
    'oj', 'ok', 'ol', 'om', 'on', 'oo', 'op', 'oq', 'or', 'os', 'ot', 'ou',
    'ov', 'ow', 'ox', 'oy', 'oz', 'pa', 'pb', 'pc', 'pd', 'pe', 'pf', 'pg',
    'ph', 'pi', 'pj', 'pk', 'pl', 'pm', 'pn', 'po', 'pp', 'pq', 'pr', 'ps',
    'pt', 'pu', 'pv', 'pw', 'px', 'py', 'pz', 'qa', 'qb', 'qc', 'qd', 'qe',
    'qf', 'qg', 'qh', 'qi', 'qj', 'qk', 'ql', 'qm', 'qn', 'qo', 'qp', 'qq',
    'qr', 'qs', 'qt', 'qu', 'qv', 'qw', 'qx', 'qy', 'qz', 'ra', 'rb', 'rc',
    'rd', 're', 'rf', 'rg', 'rh', 'ri', 'rj', 'rk', 'rl', 'rm', 'rn', 'ro',
    'rp', 'rq', 'rr', 'rs', 'rt', 'ru', 'rv', 'rw', 'rx', 'ry', 'rz', 'sa',
    'sb', 'sc', 'sd', 'se', 'sf', 'sg', 'sh', 'si', 'sj', 'sk', 'sl', 'sm',
    'sn', 'so', 'sp', 'sq', 'sr', 'ss', 'st', 'su', 'sv', 'sw', 'sx', 'sy',
    'sz', 'ta', 'tb', 'tc', 'td', 'te', 'tf', 'tg', 'th', 'ti', 'tj', 'tk',
    'tl', 'tm', 'tn', 'to', 'tp', 'tq', 'tr', 'ts', 'tt', 'tu', 'tv', 'tw',
    'tx', 'ty', 'tz', 'ua', 'ub', 'uc', 'ud', 'ue', 'uf', 'ug', 'uh', 'ui',
    'uj', 'uk', 'ul', 'um', 'un', 'uo', 'up', 'uq', 'ur', 'us', 'ut', 'uu',
    'uv', 'uw', 'ux', 'uy', 'uz', 'va', 'vb', 'vc', 'vd', 've', 'vf', 'vg',
    'vh', 'vi', 'vj', 'vk', 'vl', 'vm', 'vn', 'vo', 'vp', 'vq', 'vr', 'vs',
    'vt', 'vu', 'vv', 'vw', 'vx', 'vy', 'vz', 'wa', 'wb', 'wc', 'wd', 'we',
    'wf', 'wg', 'wh', 'wi', 'wj', 'wk', 'wl', 'wm', 'wn', 'wo', 'wp', 'wq',
    'wr', 'ws', 'wt', 'wu', 'wv', 'ww', 'wx', 'wy', 'wz', 'xa', 'xb', 'xc',
    'xd', 'xe', 'xf', 'xg', 'xh', 'xi', 'xj', 'xk', 'xl', 'xm', 'xn', 'xo',
    'xp', 'xq', 'xr', 'xs', 'xt', 'xu', 'xv', 'xw', 'xx', 'xy', 'xz', 'ya',
    'yb', 'yc', 'yd', 'ye', 'yf', 'yg', 'yh', 'yi', 'yj', 'yk', 'yl', 'ym',
    'yn', 'yo', 'yp', 'yq', 'yr', 'ys', 'yt', 'yu', 'yv', 'yw', 'yx', 'yy',
    'yz', 'za', 'zb', 'zc', 'zd', 'ze', 'zf', 'zg', 'zh', 'zi', 'zj', 'zk',
    'zl', 'zm', 'zn', 'zo', 'zp', 'zq', 'zr', 'zs', 'zt', 'zu', 'zv', 'zw',
    'zx', 'zy', 'zz',
}

# Minimum and maximum username length
MIN_USERNAME_LENGTH = 4
MAX_USERNAME_LENGTH = 30

def is_reserved_username(username):
    """Check if username is in the reserved list"""
    return username.lower() in RESERVED_USERNAMES

def is_valid_username_length(username):
    """Check if username length is valid"""
    return MIN_USERNAME_LENGTH <= len(username) <= MAX_USERNAME_LENGTH