<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>KRITZAAR — Explore</title>
  <script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.5/gsap.min.js"></script>
  <script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.5/ScrollTrigger.min.js"></script>
  <link href="https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&family=Rajdhani:wght@300;400;500;600&display=swap" rel="stylesheet">

  <style>
    :root {
      --bg:         #1A1C1E;
      --card:       #1E2124;
      --card2:      #222528;
      --mint:       #00FFC2;
      --slate:      #9BA4B0;
      --white:      #E8ECF0;
      --mint-glow:  rgba(0,255,194,0.28);
      --mint-dim:   rgba(0,255,194,0.07);
      --gold:       #C9A227;
      --gold-dim:   rgba(201,162,39,0.12);
      --gold-glow:  rgba(201,162,39,0.28);
      --nav-h:      68px;
      --hub-tab-h:  52px;
    }

    *, *::before, *::after { margin:0; padding:0; box-sizing:border-box; }
    html { scroll-behavior: smooth; }
    body { background:var(--bg); color:var(--slate); font-family:'Rajdhani',sans-serif; overflow-x:hidden; cursor:none; }

    /* ── CURSOR ── */
    #cur     { position:fixed; width:10px; height:10px; border-radius:50%; background:var(--mint); pointer-events:none; z-index:9999; transform:translate(-50%,-50%); box-shadow:0 0 14px var(--mint),0 0 30px var(--mint-glow); transition:width .2s,height .2s; }
    #curRing { position:fixed; width:36px; height:36px; border-radius:50%; border:1px solid rgba(0,255,194,0.35); pointer-events:none; z-index:9998; transform:translate(-50%,-50%); }
    body.gold-mode #cur { background:var(--gold); box-shadow:0 0 14px var(--gold),0 0 30px var(--gold-glow); }
    body.gold-mode #curRing { border-color:rgba(201,162,39,0.35); }

    /* ── GRID BG ── */
    .grid-bg { position:fixed; inset:0; background-image:linear-gradient(rgba(0,255,194,0.025) 1px,transparent 1px),linear-gradient(90deg,rgba(0,255,194,0.025) 1px,transparent 1px); background-size:64px 64px; z-index:0; pointer-events:none; }

    /* ══════════════════════════════
       TOP NAV — 8 tab buttons
    ══════════════════════════════ */
    nav {
      position:fixed; top:0; left:0; right:0; z-index:800;
      height:var(--nav-h);
      display:flex; align-items:center;
      padding:0 28px 0 28px;
      backdrop-filter:blur(18px);
      background:rgba(26,28,30,0.92);
      border-bottom:1px solid rgba(0,255,194,0.065);
      gap:20px;
    }
    .nav-logo {
      font-family:'Orbitron',sans-serif; font-size:13px; font-weight:700;
      color:var(--mint); letter-spacing:5px; flex-shrink:0;
      text-shadow:0 0 14px var(--mint-glow);
    }
    .nav-divider { width:1px; height:24px; background:rgba(255,255,255,0.06); flex-shrink:0; }
    .nav-tabs {
      display:flex; gap:2px; overflow-x:auto; flex:1;
      scrollbar-width:none;
    }
    .nav-tabs::-webkit-scrollbar { display:none; }

    .ntab {
      padding:10px 14px;
      font-family:'Rajdhani',sans-serif; font-size:11px; font-weight:600;
      letter-spacing:2px; text-transform:uppercase;
      color:var(--slate); background:none; border:none;
      border-bottom:2px solid transparent;
      cursor:none; white-space:nowrap; flex-shrink:0;
      transition:color .22s, border-color .22s;
      position:relative;
    }
    .ntab:hover  { color:var(--mint); }
    .ntab.active { color:var(--mint); border-bottom-color:var(--mint); }

    .ntab.gold-tab              { color:rgba(201,162,39,0.65); }
    .ntab.gold-tab:hover        { color:var(--gold); }
    .ntab.gold-tab.active       { color:var(--gold); border-bottom-color:var(--gold); }
    .ntab.gold-tab .gtag        { font-size:9px; margin-right:4px; }

    /* ══════════════════════════════
       MINI HERO — site identity bar
    ══════════════════════════════ */
    .krz-bar {
      position:relative; z-index:1;
      margin-top:var(--nav-h);
      padding:52px 52px 40px;
      border-bottom:1px solid rgba(0,255,194,0.055);
      display:flex; align-items:flex-end; justify-content:space-between;
    }
    .krz-wordmark {
      font-family:'Orbitron',sans-serif;
      font-size:clamp(36px,6vw,80px); font-weight:900;
      color:var(--white); letter-spacing:-2px; line-height:1;
    }
    .krz-wordmark .ac { color:var(--mint); text-shadow:0 0 24px var(--mint),0 0 60px var(--mint-glow); }
    .krz-meta { text-align:right; }
    .krz-meta p { font-size:10px; letter-spacing:5px; color:var(--slate); text-transform:uppercase; margin-bottom:8px; }
    .krz-meta a {
      font-size:10px; letter-spacing:4px; color:var(--mint);
      text-decoration:none; text-transform:uppercase;
      border-bottom:1px solid rgba(0,255,194,0.3);
      padding-bottom:2px;
      transition:border-color .25s;
    }
    .krz-meta a:hover { border-color:var(--mint); }

    /* ══════════════════════════════
       HUB — sticky tab bar + feed
    ══════════════════════════════ */
    .hub { position:relative; z-index:1; }

    /* Sticky secondary tab bar */
    .hub-tabbar {
      position:sticky; top:var(--nav-h); z-index:700;
      height:var(--hub-tab-h);
      display:flex; align-items:center;
      padding:0 52px;
      background:rgba(26,28,30,0.96);
      backdrop-filter:blur(16px);
      border-bottom:1px solid rgba(0,255,194,0.055);
      gap:0; overflow-x:auto;
      scrollbar-width:none;
    }
    .hub-tabbar::-webkit-scrollbar { display:none; }

    .htab {
      padding:0 18px; height:100%;
      font-family:'Rajdhani',sans-serif; font-size:11px; font-weight:600;
      letter-spacing:2.5px; text-transform:uppercase;
      color:var(--slate); background:none; border:none;
      border-bottom:2px solid transparent;
      cursor:none; white-space:nowrap; flex-shrink:0;
      display:flex; align-items:center;
      transition:color .22s, border-color .22s;
    }
    .htab:hover  { color:var(--mint); }
    .htab.active { color:var(--mint); border-bottom-color:var(--mint); }
    .htab.gold-tab              { color:rgba(201,162,39,0.6); }
    .htab.gold-tab:hover        { color:var(--gold); }
    .htab.gold-tab.active       { color:var(--gold); border-bottom-color:var(--gold); }

    /* Panel header */
    .panel-hdr {
      padding:36px 52px 24px;
      display:flex; align-items:baseline; gap:16px;
      border-bottom:1px solid rgba(255,255,255,0.035);
    }
    .panel-name {
      font-family:'Orbitron',sans-serif;
      font-size:clamp(22px,3vw,38px); font-weight:900;
      color:var(--white); letter-spacing:4px; text-transform:uppercase;
    }
    .panel-name.gold-head { color:var(--gold); text-shadow:0 0 20px var(--gold-glow); }
    .panel-count {
      font-size:10px; letter-spacing:4px; color:var(--slate); text-transform:uppercase;
    }

    /* Gold non-suggested banner */
    .pol-banner {
      margin:0 52px 0;
      padding:14px 20px;
      border:1px solid rgba(201,162,39,0.25);
      background:rgba(201,162,39,0.04);
      display:flex; align-items:center; gap:14px;
      display:none;
    }
    .pol-banner.visible { display:flex; }
    .pol-banner-icon { font-size:16px; flex-shrink:0; }
    .pol-banner p { font-size:11px; letter-spacing:1.5px; color:rgba(201,162,39,0.75); line-height:1.6; }
    .pol-banner strong { color:var(--gold); }

    /* Feed grid */
    .feed-panel { display:none; padding:32px 52px 0; }
    .feed-panel.active { display:block; }

    .feed-grid {
      display:grid;
      grid-template-columns:repeat(3,1fr);
      gap:20px;
      margin-bottom:48px;
    }

    /* ── CARD ── */
    .card {
      background:var(--card);
      border:1px solid rgba(0,255,194,0.065);
      border-radius:1px;
      overflow:hidden;
      transition:border-color .28s, transform .28s;
      cursor:none;
    }
    .card:hover {
      border-color:rgba(0,255,194,0.32);
      transform:translateY(-5px);
    }
    .card:hover .card-thumb-inner { transform:scale(1.04); }
    .card:hover .card-cta { color:var(--mint); letter-spacing:4px; }

    .card.card-gold { border-color:rgba(201,162,39,0.1); }
    .card.card-gold:hover { border-color:rgba(201,162,39,0.38); }
    .card.card-gold:hover .card-cta { color:var(--gold); }

    /* THUMB */
    .card-thumb { height:158px; overflow:hidden; position:relative; }
    .card-thumb-inner {
      width:100%; height:100%;
      transition:transform .45s ease;
      position:relative;
    }
    /* category gradients */
    .th-stories     { background:linear-gradient(138deg,#091e14 0%,#1a1c1e 100%); }
    .th-updates     { background:linear-gradient(225deg,#0a1828 0%,#1a1c1e 100%); }
    .th-conflict    { background:linear-gradient(45deg, #1a1008 0%,#1a1c1e 100%); }
    .th-fun         { background:linear-gradient(315deg,#180a26 0%,#1a1c1e 100%); }
    .th-coolstuff   { background:linear-gradient(180deg,#08181a 0%,#1a1c1e 100%); }
    .th-ai          { background:linear-gradient(90deg, #06121e 0%,#1a1c1e 100%); }
    .th-interesting { background:linear-gradient(270deg,#0a1818 0%,#1a1c1e 100%); }
    .th-political   { background:linear-gradient(180deg,#1c1606 0%,#1a1c1e 100%); }

    /* diagonal line texture overlay */
    .card-thumb-inner::before {
      content:''; position:absolute; inset:0;
      background:repeating-linear-gradient(-48deg,transparent,transparent 18px,rgba(0,255,194,0.018) 18px,rgba(0,255,194,0.018) 19px);
    }
    .card-gold .card-thumb-inner::before {
      background:repeating-linear-gradient(-48deg,transparent,transparent 18px,rgba(201,162,39,0.025) 18px,rgba(201,162,39,0.025) 19px);
    }

    /* card number watermark */
    .card-num {
      position:absolute; bottom:10px; right:14px;
      font-family:'Orbitron',sans-serif; font-size:36px; font-weight:900;
      color:rgba(0,255,194,0.06); letter-spacing:-2px; line-height:1;
      user-select:none;
    }
    .card-gold .card-num { color:rgba(201,162,39,0.07); }

    /* category badge on thumb */
    .thumb-badge {
      position:absolute; top:14px; left:14px;
      font-family:'Rajdhani',sans-serif; font-size:9px; font-weight:600;
      letter-spacing:3px; text-transform:uppercase;
      color:var(--mint); background:rgba(0,0,0,0.55);
      padding:4px 10px; border-left:2px solid var(--mint);
    }
    .card-gold .thumb-badge { color:var(--gold); border-color:var(--gold); }

    /* CARD BODY */
    .card-body { padding:18px 20px 20px; }
    .card-meta-row {
      display:flex; justify-content:space-between; align-items:center;
      margin-bottom:10px;
    }
    .card-tag {
      font-size:9px; letter-spacing:3.5px; text-transform:uppercase;
      color:var(--mint);
    }
    .card-gold .card-tag { color:var(--gold); }
    .card-time { font-size:9px; letter-spacing:2px; color:rgba(155,164,176,0.5); }
    .card-title {
      font-family:'Orbitron',sans-serif; font-size:12px; font-weight:700;
      color:var(--white); letter-spacing:0.3px; line-height:1.55;
      margin-bottom:14px;
    }
    .card-cta {
      font-family:'Rajdhani',sans-serif; font-size:10px; font-weight:600;
      letter-spacing:3px; text-transform:uppercase;
      color:var(--slate); background:none; border:none; cursor:none;
      padding:0; transition:color .25s, letter-spacing .25s;
    }

    /* LOAD MORE */
    .load-wrap {
      padding:0 52px 80px;
      display:flex; justify-content:center;
    }
    .load-btn {
      padding:14px 52px;
      border:1px solid rgba(0,255,194,0.25); background:none;
      color:var(--mint); font-family:'Rajdhani',sans-serif;
      font-size:11px; font-weight:600; letter-spacing:4px; text-transform:uppercase;
      cursor:none; position:relative; overflow:hidden;
      transition:color .3s;
    }
    .load-btn::before {
      content:''; position:absolute; inset:0;
      background:var(--mint); transform:translateX(-101%);
      transition:transform .35s cubic-bezier(.77,0,.175,1);
      z-index:-1;
    }
    .load-btn:hover { color:var(--bg); }
    .load-btn:hover::before { transform:translateX(0); }
    .load-btn.gold-btn { border-color:rgba(201,162,39,0.3); color:var(--gold); }
    .load-btn.gold-btn::before { background:var(--gold); }
    .load-btn.gold-btn:hover { color:var(--bg); }

    /* STATUS */
    .status { position:fixed; bottom:28px; right:52px; z-index:500; font-size:9px; letter-spacing:3px; color:var(--slate); text-transform:uppercase; display:flex; align-items:center; gap:10px; }
    .s-dot  { width:6px; height:6px; border-radius:50%; background:var(--mint); box-shadow:0 0 8px var(--mint); animation:blink 1.6s ease-in-out infinite; }
    @keyframes blink { 0%,100%{opacity:1} 50%{opacity:0.1} }

    /* ══ POLITICAL DISCLAIMER MODAL ══ */
    #polModal {
      position:fixed; inset:0; z-index:1000;
      background:rgba(0,0,0,0.75);
      backdrop-filter:blur(6px);
      display:none; align-items:center; justify-content:center;
    }
    #polModal.show { display:flex; }
    .pol-box {
      background:#1C1D20;
      border:1px solid var(--gold);
      max-width:480px; width:90%;
      padding:44px 40px 40px;
      text-align:center;
      box-shadow:0 0 60px rgba(201,162,39,0.12);
      position:relative;
    }
    .pol-icon  { font-size:28px; margin-bottom:18px; color:var(--gold); }
    .pol-box h3 {
      font-family:'Orbitron',sans-serif; font-size:13px; font-weight:900;
      color:var(--gold); letter-spacing:7px; text-transform:uppercase;
      margin-bottom:18px;
    }
    .pol-box p {
      font-size:13px; letter-spacing:1px; color:var(--slate);
      line-height:1.75; margin-bottom:10px;
    }
    .pol-box .pol-disclaimer {
      font-size:10px; letter-spacing:2px; color:rgba(155,164,176,0.5);
      margin-bottom:32px;
    }
    .pol-confirm {
      padding:13px 36px;
      border:1px solid var(--gold); background:none;
      color:var(--gold); font-family:'Rajdhani',sans-serif;
      font-size:11px; font-weight:600; letter-spacing:4px; text-transform:uppercase;
      cursor:none; position:relative; overflow:hidden;
      transition:color .28s;
    }
    .pol-confirm::before {
      content:''; position:absolute; inset:0; background:var(--gold);
      transform:translateX(-101%);
      transition:transform .35s cubic-bezier(.77,0,.175,1); z-index:-1;
    }
    .pol-confirm:hover { color:var(--bg); }
    .pol-confirm:hover::before { transform:translateX(0); }
    .pol-cancel {
      margin-top:14px; display:block;
      font-size:10px; letter-spacing:3px; color:rgba(155,164,176,0.4);
      text-transform:uppercase; cursor:none; background:none; border:none;
      transition:color .25s;
    }
    .pol-cancel:hover { color:var(--slate); }

    /* ── RESPONSIVE ── */
    @media (max-width: 900px) {
      .feed-grid { grid-template-columns:repeat(2,1fr); }
      .krz-bar, .panel-hdr, .feed-panel, .load-wrap, .pol-banner { padding-left:24px; padding-right:24px; }
      .hub-tabbar { padding:0 24px; }
    }
    @media (max-width: 580px) {
      .feed-grid { grid-template-columns:1fr; }
    }
  </style>
</head>
<body>

  <div id="cur"></div>
  <div id="curRing"></div>
  <div class="grid-bg"></div>

  <!-- ══ TOP NAV ══ -->
  <nav>
    <div class="nav-logo">KRZ</div>
    <div class="nav-divider"></div>
    <div class="nav-tabs">
      <button class="ntab active"   data-tab="stories">Stories</button>
      <button class="ntab"          data-tab="updates">Updates</button>
      <button class="ntab"          data-tab="conflict">Conflict</button>
      <button class="ntab"          data-tab="fun">Fun</button>
      <button class="ntab"          data-tab="coolstuff">Cool Stuff</button>
      <button class="ntab"          data-tab="ai">AI</button>
      <button class="ntab"          data-tab="interesting">Interesting</button>
      <button class="ntab gold-tab" data-tab="political"><span class="gtag">⚠</span>Update</button>
    </div>
  </nav>

  <!-- STATUS -->
  <div class="status"><div class="s-dot"></div><span>PART 03 — HUB</span></div>

  <!-- ══ KRZ BAR ══ -->
  <div class="krz-bar">
    <h1 class="krz-wordmark">KRITZ<span class="ac">A</span>AR</h1>
    <div class="krz-meta">
      <p>Dark-mode content hub</p>
      <a href="#">↑ Begin the climb</a>
    </div>
  </div>

  <!-- ══ HUB ══ -->
  <div class="hub" id="hub">

    <!-- Sticky sub-tab bar -->
    <div class="hub-tabbar">
      <button class="htab active"   data-tab="stories">Stories</button>
      <button class="htab"          data-tab="updates">Updates</button>
      <button class="htab"          data-tab="conflict">Conflict</button>
      <button class="htab"          data-tab="fun">Fun</button>
      <button class="htab"          data-tab="coolstuff">Cool Stuff</button>
      <button class="htab"          data-tab="ai">AI</button>
      <button class="htab"          data-tab="interesting">Interesting</button>
      <button class="htab gold-tab" data-tab="political">⚠ Update</button>
    </div>

    <!-- Panel header -->
    <div class="panel-hdr">
      <h2 class="panel-name" id="panelName">Stories</h2>
      <span class="panel-count" id="panelCount">6 entries</span>
    </div>

    <!-- Political banner (hidden by default) -->
    <div class="pol-banner" id="polBanner">
      <div class="pol-banner-icon">⚠</div>
      <p><strong>Non-Suggested Content.</strong> This section contains political news. KRITZAAR does not promote or endorse any political position. Reader discretion is advised.</p>
    </div>

    <!-- ── PANELS ── -->
    <div id="panel-stories"     class="feed-panel active"></div>
    <div id="panel-updates"     class="feed-panel"></div>
    <div id="panel-conflict"    class="feed-panel"></div>
    <div id="panel-fun"         class="feed-panel"></div>
    <div id="panel-coolstuff"   class="feed-panel"></div>
    <div id="panel-ai"          class="feed-panel"></div>
    <div id="panel-interesting" class="feed-panel"></div>
    <div id="panel-political"   class="feed-panel"></div>

    <!-- Load more -->
    <div class="load-wrap">
      <button class="load-btn" id="loadBtn">Load More</button>
    </div>

  </div><!-- end hub -->

  <!-- ══ POLITICAL DISCLAIMER MODAL ══ -->
  <div id="polModal">
    <div class="pol-box">
      <div class="pol-icon">⚠</div>
      <h3>Political Section</h3>
      <p>This section contains political news and analysis from various sources. KRITZAAR does not suggest, promote, or endorse any political party, candidate, or ideology.</p>
      <p class="pol-disclaimer">Content is presented for informational purposes only. Proceed at your own discretion.</p>
      <button class="pol-confirm" id="polConfirm">I Understand — Show Content</button>
      <button class="pol-cancel"  id="polCancel">Go Back</button>
    </div>
  </div>


  <script>
    /* ══════════════════════════════════════════
       FEED DATA
    ══════════════════════════════════════════ */
    const FEEDS = {
      stories: {
        label: 'Stories', count: '6 stories',
        isGold: false,
        cards: [
          { tag:'Feature',       time:'14 min', title:'The Man Who Walked 4,000 Miles to Find His Purpose' },
          { tag:'Personal Essay',time:'9 min',  title:'Three Years in Isolation — What I Found There' },
          { tag:'Profile',       time:'11 min', title:'She Built an Empire From a Single Notebook' },
          { tag:'Fiction',       time:'6 min',  title:'The Night the City Forgot to Sleep' },
          { tag:'Documentary',   time:'18 min', title:'Voices From the Edge: Border Stories Nobody Tells' },
          { tag:'Reflection',    time:'7 min',  title:'When Failure Was the Only Teacher That Mattered' },
        ]
      },
      updates: {
        label: 'Updates', count: '6 updates',
        isGold: false,
        cards: [
          { tag:'Breaking',    time:'3 min', title:'Global Markets Shift as Tech Sector Pivots Hard' },
          { tag:'Science',     time:'5 min', title:'Scientists Confirm Breakthrough in Quantum Storage' },
          { tag:'Urban',       time:'4 min', title:'New Framework Changes How Cities Plan Transit' },
          { tag:'Tech',        time:'2 min', title:'Open Source Project Hits 100 Million Downloads' },
          { tag:'Environment', time:'4 min', title:'Ocean Cleanup Initiative Reports Record Results' },
          { tag:'Space',       time:'6 min', title:'Telescope Captures First Clear Image of an Exoplanet Atmosphere' },
        ]
      },
      conflict: {
        label: 'Conflict', count: '6 reports',
        isGold: false,
        cards: [
          { tag:'Field Report',   time:'12 min', title:'Dispatches From the Front: A Journalist\'s Final Notes' },
          { tag:'Analysis',       time:'10 min', title:'The Hidden Economics of Prolonged Conflict Zones' },
          { tag:'Humanitarian',   time:'8 min',  title:'How Civilians Rebuild When the Cameras Leave' },
          { tag:'Investigation',  time:'14 min', title:'Mapping the Invisible: Satellite Data in War Zones' },
          { tag:'Deep Dive',      time:'11 min', title:'Water as a Weapon: The New Frontline Nobody Discusses' },
          { tag:'Long Read',      time:'16 min', title:'Children of the Ceasefire — A Generation in Limbo' },
        ]
      },
      fun: {
        label: 'Fun', count: '6 picks',
        isGold: false,
        cards: [
          { tag:'Lifestyle', time:'5 min', title:'These 12 People Quit Corporate Jobs to Play Board Games for a Living' },
          { tag:'Gaming',    time:'3 min', title:'The Internet\'s Best Hidden Game of the Year (You\'ve Not Heard of It)' },
          { tag:'Quirky',    time:'4 min', title:'A Bakery That Only Opens When It Rains' },
          { tag:'Viral',     time:'2 min', title:'Dog Breaks World Record. Dog Does Not Care in the Slightest.' },
          { tag:'Travel',    time:'6 min', title:'How to Spend 48 Hours in a City You Initially Hated' },
          { tag:'Culture',   time:'3 min', title:'The App That Makes You Laugh at 3am — Every Time' },
        ]
      },
      coolstuff: {
        label: 'Cool Stuff', count: '6 finds',
        isGold: false,
        cards: [
          { tag:'Materials',   time:'5 min', title:'This New Material Cools Itself Without a Single Watt of Electricity' },
          { tag:'Design',      time:'7 min', title:'The Designer Who Makes Museum-Grade Furniture From Compressed Air' },
          { tag:'Architecture',time:'8 min', title:'Zero-Waste Studio Built Entirely From Reclaimed Found Objects' },
          { tag:'Photography', time:'4 min', title:'A Camera That Shoots in Near-Total Darkness — No Flash Needed' },
          { tag:'Gadgets',     time:'3 min', title:'The Keyboard That Adapts Its Layout to Your Current Mood' },
          { tag:'Wearables',   time:'6 min', title:'Solar Fabric: Clothes That Quietly Charge Your Phone as You Walk' },
        ]
      },
      ai: {
        label: 'AI', count: '6 reads',
        isGold: false,
        cards: [
          { tag:'Development', time:'8 min',  title:'LLMs Now Write Code That Autonomously Fixes Itself in Production' },
          { tag:'Safety',      time:'10 min', title:'The Model That Learned to Refuse — And Why That\'s Complicated' },
          { tag:'Science',     time:'7 min',  title:'How AI Is Reading the Ocean Floor for the First Time in History' },
          { tag:'Analysis',    time:'12 min', title:'Open Source vs Closed AI: The War That Shapes Your Future' },
          { tag:'Healthcare',  time:'9 min',  title:'Your Next Therapist May Not Be Human — and That\'s the Point' },
          { tag:'Critique',    time:'6 min',  title:'The Benchmark Problem: Why AI Scores Mean Absolutely Nothing' },
        ]
      },
      interesting: {
        label: 'Interesting Site', count: '6 discoveries',
        isGold: false,
        cards: [
          { tag:'Discovery',        time:'2 min', title:'This Site Lets You Hear Every Radio Station Simultaneously, Live' },
          { tag:'Linguistics',      time:'4 min', title:'An Interactive Map of Every Language Ever Spoken on Earth' },
          { tag:'Internet History', time:'6 min', title:'The Website Built by One Person Over 22 Continuous Years' },
          { tag:'Creative Tool',    time:'3 min', title:'Type Anything. Watch It Become a Song. (No Sign-up Required)' },
          { tag:'Tracking',         time:'2 min', title:'Real-Time Satellite View of Every Single Ship on Earth Right Now' },
          { tag:'Speculative',      time:'5 min', title:'A Wiki Entirely Dedicated to Things That Don\'t Exist Yet' },
        ]
      },
      political: {
        label: 'Update', count: '6 articles',
        isGold: true,
        cards: [
          { tag:'Policy',        time:'9 min',  title:'Policy Shifts in Global Trade Agreements: A Full Breakdown' },
          { tag:'Analysis',      time:'11 min', title:'The Widening Funding Gap in Democratic Infrastructure' },
          { tag:'Elections',     time:'8 min',  title:'Voting Systems Under Scrutiny Across Four Major Nations' },
          { tag:'Transparency',  time:'12 min', title:'Lobbying Data Released: Who Pays for Which Policy, Exactly' },
          { tag:'Economy',       time:'7 min',  title:'Central Bank Decisions and Their Immediate Political Fallout' },
          { tag:'International', time:'14 min', title:'The Quiet Reshaping of International Law Few Are Watching' },
        ]
      },
    };

    /* ══════════════════════════════════════════
       CARD GENERATION
    ══════════════════════════════════════════ */
    function buildCards(tabId, isGold) {
      const data = FEEDS[tabId];
      const thumbClass = 'th-' + tabId;
      return data.cards.map((c, i) => `
        <div class="card ${isGold ? 'card-gold' : ''}">
          <div class="card-thumb">
            <div class="card-thumb-inner ${thumbClass}">
              <div class="card-num">${String(i + 1).padStart(2,'0')}</div>
              <div class="thumb-badge">${c.tag}</div>
            </div>
          </div>
          <div class="card-body">
            <div class="card-meta-row">
              <span class="card-tag">${c.tag}</span>
              <span class="card-time">${c.time} read</span>
            </div>
            <h3 class="card-title">${c.title}</h3>
            <button class="card-cta">Read →</button>
          </div>
        </div>
      `).join('');
    }

    /* Inject all panels on load */
    Object.keys(FEEDS).forEach(id => {
      const panel = document.getElementById('panel-' + id);
      if (!panel) return;
      panel.innerHTML = `<div class="feed-grid">${buildCards(id, FEEDS[id].isGold)}</div>`;
    });

    /* ══════════════════════════════════════════
       TAB SWITCHING
    ══════════════════════════════════════════ */
    let currentTab   = 'stories';
    let polConfirmed = false;

    function switchTab(tabId) {

      /* Political gate */
      if (tabId === 'political' && !polConfirmed) {
        document.getElementById('polModal').classList.add('show');
        return;
      }

      if (tabId === currentTab) return;
      currentTab = tabId;

      const isGold = FEEDS[tabId].isGold;

      /* Update cursor theme */
      document.body.classList.toggle('gold-mode', isGold);

      /* Update all tab buttons */
      document.querySelectorAll('.ntab,.htab').forEach(btn => {
        btn.classList.toggle('active', btn.dataset.tab === tabId);
      });

      /* Update panel header */
      const pn = document.getElementById('panelName');
      pn.textContent = FEEDS[tabId].label;
      pn.className = 'panel-name' + (isGold ? ' gold-head' : '');
      document.getElementById('panelCount').textContent = FEEDS[tabId].count;

      /* Political banner */
      document.getElementById('polBanner').classList.toggle('visible', isGold);

      /* Load more button gold state */
      document.getElementById('loadBtn').className = 'load-btn' + (isGold ? ' gold-btn' : '');

      /* Hide all panels */
      document.querySelectorAll('.feed-panel').forEach(p => {
        p.classList.remove('active');
        p.style.display = 'none';
      });

      /* Show + animate target panel */
      const panel = document.getElementById('panel-' + tabId);
      panel.style.display = 'block';
      panel.classList.add('active');

      const cards = panel.querySelectorAll('.card');
      gsap.fromTo(cards,
        { y: 28, opacity: 0 },
        { y: 0, opacity: 1, duration: 0.45, ease: 'power2.out', stagger: 0.07 }
      );

      /* Scroll to hub top */
      document.getElementById('hub').scrollIntoView({ behavior:'smooth', block:'start' });
    }

    /* Attach click handlers to ALL tab buttons */
    document.querySelectorAll('.ntab,.htab').forEach(btn => {
      btn.addEventListener('click', () => switchTab(btn.dataset.tab));
    });

    /* Animate initial panel on load */
    gsap.from('#panel-stories .card', {
      y: 28, opacity: 0, duration: 0.5, ease: 'power2.out', stagger: 0.07, delay: 0.3
    });

    /* ══════════════════════════════════════════
       POLITICAL MODAL
    ══════════════════════════════════════════ */
    document.getElementById('polConfirm').addEventListener('click', () => {
      polConfirmed = true;
      document.getElementById('polModal').classList.remove('show');
      switchTab('political');
    });

    document.getElementById('polCancel').addEventListener('click', () => {
      document.getElementById('polModal').classList.remove('show');
    });

    /* ══════════════════════════════════════════
       LOAD MORE (simulated)
    ══════════════════════════════════════════ */
    document.getElementById('loadBtn').addEventListener('click', () => {
      const panel = document.getElementById('panel-' + currentTab);
      const grid  = panel.querySelector('.feed-grid');
      const isGold = FEEDS[currentTab].isGold;
      const tabId  = currentTab;

      /* Generate 3 extra placeholder cards */
      const extras = [1,2,3].map(i => `
        <div class="card ${isGold ? 'card-gold' : ''}">
          <div class="card-thumb">
            <div class="card-thumb-inner th-${tabId}">
              <div class="card-num">${String(FEEDS[tabId].cards.length + i).padStart(2,'0')}</div>
              <div class="thumb-badge">More</div>
            </div>
          </div>
          <div class="card-body">
            <div class="card-meta-row">
              <span class="card-tag">${isGold ? 'Extended' : 'More'}</span>
              <span class="card-time">${5 + i} min read</span>
            </div>
            <h3 class="card-title">Loading next wave of ${FEEDS[tabId].label.toLowerCase()} content…</h3>
            <button class="card-cta">Read →</button>
          </div>
        </div>
      `).join('');

      grid.insertAdjacentHTML('beforeend', extras);
      const newCards = Array.from(grid.querySelectorAll('.card')).slice(-3);
      gsap.fromTo(newCards,
        { y: 32, opacity: 0 },
        { y: 0, opacity: 1, duration: 0.45, ease: 'power2.out', stagger: 0.07 }
      );
    });

    /* ══════════════════════════════════════════
       CURSOR
    ══════════════════════════════════════════ */
    const cur = document.getElementById('cur');
    const crg = document.getElementById('curRing');
    let mx = window.innerWidth/2, my = window.innerHeight/2;
    let rx = mx, ry = my;
    document.addEventListener('mousemove', e => { mx = e.clientX; my = e.clientY; });
    (function loop() {
      rx += (mx-rx)*0.15; ry += (my-ry)*0.15;
      cur.style.left = mx+'px'; cur.style.top = my+'px';
      crg.style.left = rx+'px'; crg.style.top = ry+'px';
      requestAnimationFrame(loop);
    })();

    /* Scale cursor on interactive elements */
    document.querySelectorAll('button,.card').forEach(el => {
      el.addEventListener('mouseenter', () => gsap.to(cur, { width:7, height:7, duration:0.2 }));
      el.addEventListener('mouseleave', () => gsap.to(cur, { width:10, height:10, duration:0.2 }));
    });

    /* ══════════════════════════════════════════
       CARD HOVER GLOW (mint glow on card border)
    ══════════════════════════════════════════ */
    document.addEventListener('mouseover', e => {
      const card = e.target.closest('.card');
      if (card) {
        const isGold = card.classList.contains('card-gold');
        card.style.boxShadow = isGold
          ? '0 8px 32px rgba(201,162,39,0.08)'
          : '0 8px 32px rgba(0,255,194,0.07)';
      }
    });
    document.addEventListener('mouseout', e => {
      const card = e.target.closest('.card');
      if (card) card.style.boxShadow = 'none';
    });

    /* ══════════════════════════════════════════
       KRZ WORDMARK PULSE
    ══════════════════════════════════════════ */
    gsap.to('.krz-wordmark .ac', {
      textShadow:'0 0 36px #00FFC2,0 0 80px rgba(0,255,194,0.5)',
      duration:2.2, ease:'power2.inOut', repeat:-1, yoyo:true,
    });

  </script>
</body>
</html>
