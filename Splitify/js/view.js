export class SplitifyView {
    constructor() {
        this.els = {
            cash: document.getElementById('dispCash'),
            bank: document.getElementById('dispBank'),
            week: document.getElementById('dispWeek'),
            recv: document.getElementById('dispRecv'),
            friendsList: document.getElementById('listFriends'),
            historyList: document.getElementById('listHistory'),
            modalOverlay: document.getElementById('modalOverlay'),
            modalContent: document.getElementById('modalContent')
        };
    }

    applyTheme(theme) {
        if (theme === 'dark') document.documentElement.classList.add('dark');
        else document.documentElement.classList.remove('dark');
    }

    renderDashboard(data) {
        this.els.cash.innerText = data.cash.toLocaleString();
        this.els.bank.innerText = data.bank.toLocaleString();
        this.els.week.innerText = data.week.toLocaleString();
        
        let recv = 0;
        Object.values(data.people).forEach(v => { if (v > 0) recv += v; });
        this.els.recv.innerText = recv.toLocaleString();

        this.renderFriends(data.people);
        this.renderHistory(data.trans.slice().reverse().slice(0, 5)); // Recent 5
    }

    renderFriends(peopleObj) {
        this.els.friendsList.innerHTML = '';
        const sorted = Object.entries(peopleObj).sort((a, b) => b[1] - a[1]);

        if (sorted.length === 0) {
            this.els.friendsList.innerHTML = this._getEmptyState('No friends added yet.');
            return;
        }

        sorted.forEach(([name, bal]) => {
            const isOwe = bal < 0;
            const color = isOwe ? 'text-red-500' : 'text-green-600';
            const bg = isOwe ? 'bg-red-50 dark:bg-red-900/30 text-red-500' : 'bg-green-50 dark:bg-green-900/30 text-green-600';
            const status = isOwe ? 'YOU OWE' : 'OWES YOU';
            
            // Settle Up Button Logic
            const settleBtn = bal > 0 ? `<button class="btn-settle text-[10px] bg-blue-100 dark:bg-blue-900 text-blue-600 dark:text-blue-300 px-3 py-1 rounded-full font-bold ml-2" data-name="${name}" data-amt="${bal}">Settle</button>` : '';

            const html = `
                <div class="flex justify-between items-center p-4 hover:bg-slate-50 dark:hover:bg-slate-700/50 transition cursor-pointer group">
                    <div class="flex items-center gap-4">
                        <div class="w-12 h-12 rounded-full ${bg} flex items-center justify-center font-bold shadow-sm text-lg">${name[0]}</div>
                        <div>
                            <p class="font-bold text-slate-800 dark:text-slate-100">${name}</p>
                            <p class="text-[10px] text-slate-400 font-bold uppercase mt-0.5">${status}</p>
                        </div>
                    </div>
                    <div class="flex items-center">
                        <p class="font-extrabold ${color} text-lg">${Math.abs(bal).toLocaleString()}</p>
                        ${settleBtn}
                    </div>
                </div>`;
            this.els.friendsList.insertAdjacentHTML('beforeend', html);
        });
    }

    renderHistory(transList) {
        this.els.historyList.innerHTML = '';
        if (transList.length === 0) {
            this.els.historyList.innerHTML = this._getEmptyState('No transactions yet.', 'fa-receipt');
            return;
        }
        transList.forEach((t, index) => {
            let icon = 'fa-receipt', color = 'bg-slate-100 dark:bg-slate-700 text-slate-500';
            if (t.type.includes('EXPENSE')) { icon = 'fa-arrow-trend-down'; color = 'bg-red-100 dark:bg-red-900/30 text-red-500'; }
            else if (['RECEIVED', 'TRANSFER_IN'].includes(t.type)) { icon = 'fa-arrow-down'; color = 'bg-green-100 dark:bg-green-900/30 text-green-500'; }
            
            const html = `
                <div class="bg-white dark:bg-slate-800 p-4 rounded-2xl border border-slate-100 dark:border-slate-700 flex justify-between items-center shadow-sm">
                    <div class="flex items-center gap-3 overflow-hidden">
                        <div class="w-10 h-10 rounded-full ${color} flex items-center justify-center shrink-0"><i class="fa-solid ${icon}"></i></div>
                        <div class="min-w-0">
                            <p class="font-bold text-slate-700 dark:text-slate-200 truncate text-sm">${t.desc}</p>
                            <p class="text-[10px] text-slate-400 font-bold uppercase">${t.date} • ${t.person || 'Self'}</p>
                        </div>
                    </div>
                    <span class="font-bold text-slate-800 dark:text-slate-100">${parseInt(t.amt).toLocaleString()}</span>
                </div>`;
            this.els.historyList.insertAdjacentHTML('beforeend', html);
        });
    }

    _getEmptyState(msg, icon = 'fa-ghost') {
        return `<div class="p-8 text-center text-slate-400 dark:text-slate-500 font-medium">
            <i class="fa-solid ${icon} text-2xl mb-2 opacity-50"></i><br>${msg}
        </div>`;
    }

    openModal(contentHTML) {
        this.els.modalContent.innerHTML = contentHTML;
        this.els.modalOverlay.classList.add('active');
        this.els.modalContent.classList.add('active');
    }

    closeModal() {
        this.els.modalOverlay.classList.remove('active');
        this.els.modalContent.classList.remove('active');
    }
}