window.addEventListener('load', async () => {
    // কনফিগ চেক
    if (typeof window.CONFIG === 'undefined') {
        document.getElementById('status').innerText = "Error: config.js not loaded!";
        return;
    }

    const player = videojs('gemini-live-player');
    const params = new URLSearchParams(window.location.search);
    const sourceUrl = params.get('url') || "https://iptv-org.github.io/iptv/countries/in.m3u";

    try {
        // প্রক্সি দিয়ে প্লেলিস্ট ফেচ
        const proxyUrl = "https://api.allorigins.win/raw?url=" + encodeURIComponent(sourceUrl);
        const response = await fetch(proxyUrl);
        if (!response.ok) throw new Error("Connection failed");
        
        const text = await response.text();
        const container = document.getElementById('channel-container');
        const lines = text.split('\n');

        // সার্চ ফাংশনালিটি
        const searchInput = document.createElement('input');
        searchInput.placeholder = "সার্চ করুন...";
        searchInput.style = "width: 90%; padding: 10px; margin-bottom: 15px; border-radius: 5px; border: none;";
        container.parentElement.prepend(searchInput);

        searchInput.onkeyup = () => {
            const filter = searchInput.value.toUpperCase();
            const items = document.getElementsByClassName('ch-item');
            for (let i = 0; i < items.length; i++) {
                items[i].style.display = items[i].innerText.toUpperCase().includes(filter) ? "" : "none";
            }
        };

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
        document.getElementById('loader').style.display = 'none';
    } catch (e) {
        document.getElementById('status').innerText = "Sync Failed: " + e.message;
    }
});
