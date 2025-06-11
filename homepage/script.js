const form = document.querySelector("#loginForm");
let currentSongPage = 1;
const songLimit = 10;
let loadingSongs = false;
let allSongsLoaded = false;
let userId = null;
let historyData = [];

if (form) {
    form.addEventListener("submit", async (e) => {
        e.preventDefault();
        const user = document.querySelector("#username").value;
        const pass = document.querySelector("#password").value;
        const data = {
            username: user,
            password: pass
        }
        const request = await fetch("http://localhost:8000/login", {
            method: "Post",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(data)
        });
        const resp = await request.json();
        if (resp.status === "ok") {
            alert("Login successful");
            localStorage.setItem("username", data.username);
            window.location.href = "dashboard.html";
        } else {
            alert("Login failed");
        }
    });
}

// Dashboard : récupération dynamique de l'utilisateur connecté
if (window.location.pathname.includes("dashboard.html")) {
    const username = localStorage.getItem("username");
    if (!username) {
        window.location.href = "login.html";
    } else {
        fetch(`http://localhost:8000/users?username=${username}`)
            .then(res => res.json())
            .then(user => {
                if (user && user.id) {
                    userId = user.id;
                    loadDashboard(userId);
                } else {
                    alert("Utilisateur non trouvé !");
                    window.location.href = "login.html";
                }
            });
    }
}

function renderSongLi(song, interaction) {
    const li = document.createElement('li');
    li.textContent = `${song.title} - ${song.artist || ''} (${song.genre || ''})`;

    // Bouton Like
    const btnLike = document.createElement('button');
    btnLike.textContent = "Like";
    if (interaction && interaction.liked) btnLike.style.background = "gold";
    btnLike.onclick = () => {
        if (interaction && interaction.liked) {
            fetch(`http://localhost:8000/interactions/${interaction.id}`, { method: 'DELETE' })
                .then(() => location.reload());
        } else {
            fetch('http://localhost:8000/interactions', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    user_id: userId,
                    song_id: song.id,
                    liked: true,
                    interaction_time: new Date().toISOString()
                })
            }).then(() => location.reload());
        }
    };

    // Bouton Dislike
    const btnDislike = document.createElement('button');
    btnDislike.textContent = "Dislike";
    if (interaction && interaction.liked === false) btnDislike.style.background = "gold";
    btnDislike.onclick = () => {
        if (interaction && interaction.liked === false) {
            fetch(`http://localhost:8000/interactions/${interaction.id}`, { method: 'DELETE' })
                .then(() => location.reload());
        } else {
            fetch('http://localhost:8000/interactions', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    user_id: userId,
                    song_id: song.id,
                    liked: false,
                    interaction_time: new Date().toISOString()
                })
            }).then(() => location.reload());
        }
    };

    li.appendChild(btnLike);
    li.appendChild(btnDislike);
    return li;
}

function loadMoreSongs(query = "") {
    if (loadingSongs || allSongsLoaded) return;
    loadingSongs = true;
    const skip = (currentSongPage - 1) * songLimit;
    let url = query
        ? `http://localhost:8000/songs/search?q=${encodeURIComponent(query)}&skip=${skip}&limit=${songLimit}`
        : `http://localhost:8000/songs?skip=${skip}&limit=${songLimit}`;
    fetch(url)
        .then(res => res.json())
        .then(data => {
            const songs = document.getElementById('songs');
            if (songs) {
                data.forEach(song => {
                    const interaction = historyData.find(i => i.song_id === song.id);
                    const li = renderSongLi(song, interaction);
                    songs.appendChild(li);
                });
                if (data.length < songLimit) {
                    allSongsLoaded = true;
                } else {
                    currentSongPage++;
                }
            }
            loadingSongs = false;
        });
}

function loadDashboard(uid) {
    // Afficher le username dans le header
    const username = localStorage.getItem("username");
    const userHeader = document.querySelector('.user-box h3');
    if (userHeader && username) {
        userHeader.textContent = username;
    }

    // Afficher les recommandations
    fetch(`http://localhost:8000/recommendations/${uid}`)
        .then(res => res.json())
        .then(data => {
            const reco = document.getElementById('recommendations');
            if (reco) {
                reco.innerHTML = "";
                if (data.recommended_songs && data.recommended_songs.length > 0) {
                    data.recommended_songs.forEach(songId => {
                        const li = document.createElement('li');
                        li.textContent = "Chanson ID: " + songId;
                        reco.appendChild(li);
                    });
                } else {
                    reco.innerHTML = "<li>Aucune recommandation</li>";
                }
            }
        });

    // Afficher l'historique et initialiser le scroll infini pour les chansons
    fetch(`http://localhost:8000/interactions/${uid}`)
        .then(res => res.json())
        .then(data => {
            historyData = data;
            const hist = document.getElementById('history');
            if (hist) {
                hist.innerHTML = "";
                if (data.length > 0) {
                    data.forEach(inter => {
                        const li = document.createElement('li');
                        li.textContent = `Chanson ID: ${inter.song_id} | Liked: ${inter.liked}`;
                        hist.appendChild(li);
                    });
                } else {
                    hist.innerHTML = "<li>Aucune interaction</li>";
                }
            }
            // Initialisation scroll infini chansons
            currentSongPage = 1;
            allSongsLoaded = false;
            const songsDiv = document.getElementById('songs');
            songsDiv.innerHTML = "";
            loadMoreSongs();

            // Scroll infini sur la section chansons
            songsDiv.onscroll = function () {
                if (songsDiv.scrollTop + songsDiv.clientHeight >= songsDiv.scrollHeight - 10) {
                    loadMoreSongs();
                }
            };
        });
}

// Recherche dynamique de chansons (remplace la liste et désactive le scroll infini)
const searchInput = document.getElementById('searchInput');
if (searchInput) {
    searchInput.addEventListener('input', function () {
        const query = searchInput.value.trim();
        const songsDiv = document.getElementById('songs');
        songsDiv.innerHTML = "";
        currentSongPage = 1;
        allSongsLoaded = false;
        if (query.length === 0) {
            // Recharge toutes les chansons si la recherche est vide
            loadDashboard(userId);
        } else {
            // Désactive le scroll infini pendant la recherche
            songsDiv.onscroll = null;
            fetch(`http://localhost:8000/interactions/${userId}`)
                .then(res => res.json())
                .then(histData => {
                    historyData = histData;
                    fetch(`http://localhost:8000/songs/search?q=${encodeURIComponent(query)}`)
                        .then(res => res.json())
                        .then(data => {
                            if (songsDiv) {
                                data.forEach(song => {
                                    const interaction = historyData.find(i => i.song_id === song.id);
                                    const li = renderSongLi(song, interaction);
                                    songsDiv.appendChild(li);
                                });
                            }
                        });
                });
        }
    });
}
