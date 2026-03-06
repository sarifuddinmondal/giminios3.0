window.addEventListener('load', async () => {
    // ভিডিও প্লেয়ার ইনিশিয়ালাইজেশন
    const player = videojs('gemini-live-player');
    
    // ইউআরএল থেকে সোর্স নেওয়া অথবা ডিফল্ট সোর্স
    const params = new URLSearchParams(window.location.search);
    const sourceUrl = params.get('url') || "https://iptv-org.github.io/iptv/countries/in.m3u";

    const container = document.getElementById('channel-container');
    const loaderStatus = document.getElementById('status');

    try {
        // একাধিক প্রক্সি সার্ভার সেট করা যাতে একটি ডাউন থাকলে অন্যটি কাজ করে
        const proxies = [
            "https://api.allorigins.win/raw?url=",
            "https://corsproxy.io/?"
        ];
        
        let text = null;
        for (let proxy of proxies) {
            try {
                const response = await fetch(proxy + encodeURIComponent(sourceUrl));
                if (response.ok) {
                    text = await response.text();
                    break;
                }
            } catch (e) { continue; }
        }

        if (!text) throw new Error("Could not connect to playlist source");
        
        const lines = text.split('\n');

        // সার্চ বার তৈরি (যদি আগে তৈরি না থাকে)
        if (!document.getElementById('search-box')) {
            const searchInput = document.createElement('input');
            searchInput.id = "search-box";
            searchInput.placeholder = "চ্যানেল সার্চ করুন...";
            searchInput.style = "width: 90%; padding: 10px; margin-bottom: 15px; border-radius: 5px; border: none; background: #222; color: white;";
            container.parentElement.prepend(searchInput);

            // সার্চ লজিক
            searchInput.onkeyup = () => {
                const filter = searchInput.value.toUpperCase();
                const items = document.getElementsByClassName('ch-item');
                for (let i = 0; i < items.length; i++) {
                    items[i].style.display = items[i].innerText.toUpperCase().includes(filter) ? "" : "none";
                }
            };
        }

        // চ্যানেল লোড করা
        lines.forEach((line, index) => {
            if (line.startsWith('#EXTINF:')) {
                let name = line.split(',')[1] || "Unnamed Channel";
                let nextLine = lines[index + 1];
                if (nextLine && nextLine.startsWith('http')) {
                    let btn = document.createElement('div');
                    btn.className = 'ch-item';
                    btn.innerText = name;
                    btn.onclick = () => { 
                        player.src({src: nextLine.trim(), type: 'application/x-mpegURL'}); 
                        player.play(); 
                        document.getElementById('playlist-drawer').classList.remove('open');
                    };
                    container.appendChild(btn);
                }
            }
        });
        
        // লোডার হাইড করা
        document.getElementById('loader').style.display = 'none';
        
    } catch (e) {
        loaderStatus.innerText = "Sync Failed: " + e.message;
        console.error("IPTV Loader Error:", e);
    }
});
