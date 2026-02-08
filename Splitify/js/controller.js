import { SplitifyModel } from './model.js';
import { SplitifyView } from './view.js';

const app = new SplitifyModel();
const view = new SplitifyView();

window.onload = () => {
    init();
};

function init() {
    // Initial Render
    view.applyTheme(app.data.theme);
    view.renderDashboard(app.calculateTotals());
    
    // Event Listeners - Navigation
    document.getElementById('navExpense').onclick = () => openExpenseForm();
    document.getElementById('navSplit').onclick = () => openSplitForm();
    document.getElementById('navMenu').onclick = () => openMenuModal();
    document.getElementById('btnSettings').onclick = () => openSettings();
    document.getElementById('modalOverlay').onclick = (e) => { if(e.target.id === 'modalOverlay') view.closeModal(); };

    // Delegate "Settle Up" clicks in the friends list
    document.getElementById('listFriends').addEventListener('click', (e) => {
        if(e.target.classList.contains('btn-settle')) {
            const name = e.target.dataset.name;
            const amt = e.target.dataset.amt;
            openSettleUpForm(name, amt);
            e.stopPropagation(); // Prevent opening detail view
        }
    });
}

// --- FORM BUILDERS ---

function openExpenseForm() {
    const html = `
        <div class="p-6 border-b border-slate-100 dark:border-slate-700 flex justify-between items-center bg-slate-50/50 dark:bg-slate-800 rounded-t-[2rem]">
            <h3 class="font-bold text-lg text-slate-800 dark:text-white">Add Expense</h3>
            <button onclick="document.getElementById('modalOverlay').click()" class="w-8 h-8 rounded-full bg-slate-200 dark:bg-slate-700 flex items-center justify-center text-slate-500"><i class="fa-solid fa-times"></i></button>
        </div>
        <div class="p-6 space-y-6 overflow-y-auto flex-1 dark:text-slate-200">
            <div>
                <label class="text-xs font-bold text-slate-400 uppercase">Amount</label>
                <div class="relative mt-1">
                    <span class="absolute left-4 top-1/2 -translate-y-1/2 text-slate-400 font-bold text-xl">Rs</span>
                    <input type="number" id="inpAmt" class="w-full pl-12 pr-4 py-4 bg-slate-50 dark:bg-slate-700 border border-transparent focus:border-blue-500 dark:border-slate-600 rounded-2xl font-bold text-2xl outline-none" placeholder="0" autofocus>
                </div>
            </div>
            <div>
                <label class="text-xs font-bold text-slate-400 uppercase">Description</label>
                <input type="text" id="inpDesc" class="w-full mt-1 p-4 bg-slate-50 dark:bg-slate-700 rounded-2xl font-bold outline-none" placeholder="Lunch, Taxi, etc.">
            </div>
            <div class="flex gap-2">
                <select id="inpSource" class="flex-1 p-3 bg-slate-100 dark:bg-slate-700 rounded-xl font-bold text-sm"><option value="CASH">Cash</option><option value="BANK">Bank</option></select>
                <select id="inpTag" class="flex-1 p-3 bg-slate-100 dark:bg-slate-700 rounded-xl font-bold text-sm">
                    ${app.data.tags.map(t => `<option value="${t}">${t}</option>`).join('')}
                </select>
            </div>
            <button id="btnSubmitExp" class="w-full bg-blue-600 text-white font-bold text-lg py-4 rounded-2xl shadow-lg mt-4">Confirm Expense</button>
        </div>
    `;
    view.openModal(html);
    
    document.getElementById('btnSubmitExp').onclick = () => {
        const amt = parseInt(document.getElementById('inpAmt').value);
        if(!amt) return;
        app.addTransaction({
            date: new Date().toLocaleDateString('en-GB', { day: 'numeric', month: 'short' }),
            type: 'EXPENSE',
            amt: amt,
            desc: document.getElementById('inpDesc').value || 'Expense',
            person: 'Self',
            source: document.getElementById('inpSource').value,
            tag: document.getElementById('inpTag').value
        });
        view.closeModal();
        view.renderDashboard(app.calculateTotals());
    };
}

function openSplitForm() {
    // Advanced Split Form with "Exact Amount" inputs
    const people = Object.keys(app.data.people);
    let friendsHtml = people.map(p => `
        <div class="checkbox-wrapper flex items-center justify-between p-3 border dark:border-slate-700 rounded-xl bg-slate-50 dark:bg-slate-700/30 mb-2">
            <label class="flex items-center gap-3 cursor-pointer flex-1">
                <input type="checkbox" class="split-check w-5 h-5 accent-blue-600 rounded" value="${p}" checked>
                <span class="font-bold text-sm dark:text-slate-200">${p}</span>
            </label>
            <input type="number" class="split-amt-manual w-20 p-2 text-right bg-white dark:bg-slate-800 border rounded-lg text-xs font-bold" placeholder="Auto" data-person="${p}">
        </div>
    `).join('');

    const html = `
        <div class="p-6 border-b border-slate-100 dark:border-slate-700 flex justify-between items-center bg-slate-50/50 dark:bg-slate-800 rounded-t-[2rem]">
            <h3 class="font-bold text-lg text-slate-800 dark:text-white">Split Bill</h3>
            <button onclick="document.getElementById('modalOverlay').click()" class="w-8 h-8 rounded-full bg-slate-200 dark:bg-slate-700 flex items-center justify-center text-slate-500"><i class="fa-solid fa-times"></i></button>
        </div>
        <div class="p-6 overflow-y-auto flex-1">
            <input type="number" id="inpSplitAmt" class="w-full p-4 bg-slate-50 dark:bg-slate-700 rounded-2xl font-bold text-2xl mb-4 outline-none" placeholder="Total Amount">
            <input type="text" id="inpSplitDesc" class="w-full p-4 bg-slate-50 dark:bg-slate-700 rounded-2xl font-bold mb-4 outline-none" placeholder="Description">
            
            <label class="text-xs font-bold text-slate-400 uppercase mb-2 block">Split With</label>
            <div class="max-h-60 overflow-y-auto">${friendsHtml}</div>
            
            <button id="btnSubmitSplit" class="w-full bg-purple-600 text-white font-bold text-lg py-4 rounded-2xl shadow-lg mt-6">Split It</button>
        </div>
    `;
    view.openModal(html);

    document.getElementById('btnSubmitSplit').onclick = () => {
        const total = parseInt(document.getElementById('inpSplitAmt').value);
        if(!total) return;

        // Gather manual inputs
        const checks = document.querySelectorAll('.split-check:checked');
        const manualInputs = document.querySelectorAll('.split-amt-manual');
        let manualMap = {};
        let manualSum = 0;
        let count = 0;

        // Build map of specific values
        manualInputs.forEach(input => {
            const p = input.dataset.person;
            const isChecked = [...checks].some(c => c.value === p);
            if(isChecked && input.value) {
                const val = parseInt(input.value);
                manualMap[p] = val;
                manualSum += val;
            } else if(isChecked) {
                count++; // Needs auto calc
            }
        });

        // Add Self to calculation (My Share)
        // Simple logic: Total - Sum(Friend Shares) = My Share
        // Or should I include myself in the split? 
        // For this version, let's assume I paid the full amount, so I am just recovering Friend Shares.
        
        let remaining = total - manualSum;
        let autoShare = count > 0 ? Math.round(remaining / (count + 1)) : 0; // +1 for Self

        // If user manually entered EVERYONE, we might have remainder issues.
        
        const date = new Date().toLocaleDateString('en-GB', { day: 'numeric', month: 'short' });
        const desc = document.getElementById('inpSplitDesc').value || 'Split';

        // 1. Deduct Total from Wallet
        app.addTransaction({ date, type: 'SPLIT_MAIN', amt: total, desc: desc + ' (Total)', person: 'Self', source: 'CASH' });

        // 2. Add Debt for each friend
        checks.forEach(c => {
            const p = c.value;
            const amt = manualMap[p] ? manualMap[p] : autoShare;
            app.addTransaction({ date, type: 'SPLIT_DEBIT', amt: amt, desc: desc, person: p });
            remaining -= amt; // Deduct from what I paid
        });

        // 3. Record My Share (What's left of what I paid)
        app.addTransaction({ date, type: 'SPLIT_SHARE', amt: remaining, desc: desc + ' (My Share)', person: 'Self' });

        view.closeModal();
        view.renderDashboard(app.calculateTotals());
    };
}

function openSettleUpForm(name, amount) {
    const html = `
        <div class="p-6 bg-white dark:bg-slate-800 rounded-t-[2rem]">
            <h3 class="font-bold text-lg text-center mb-4 dark:text-white">Settle with ${name}</h3>
            <p class="text-center text-slate-500 text-sm mb-6">Confirm you received payment</p>
            <div class="text-center text-4xl font-extrabold text-green-600 mb-8">${amount}</div>
            <button id="btnConfirmSettle" class="w-full bg-green-600 text-white font-bold py-4 rounded-2xl shadow-lg">Confirm Received</button>
        </div>
    `;
    view.openModal(html);
    
    document.getElementById('btnConfirmSettle').onclick = () => {
        app.addTransaction({
            date: new Date().toLocaleDateString('en-GB', { day: 'numeric', month: 'short' }),
            type: 'RECEIVED',
            amt: amount,
            desc: 'Settlement',
            person: name,
            source: 'CASH'
        });
        view.closeModal();
        view.renderDashboard(app.calculateTotals());
    };
}

function openSettings() {
    const isDark = app.data.theme === 'dark';
    const html = `
        <div class="p-6 bg-white dark:bg-slate-800 rounded-t-[2rem] text-center">
            <h3 class="font-bold text-lg mb-6 dark:text-white">Settings</h3>
            <button id="btnTheme" class="w-full p-4 bg-slate-100 dark:bg-slate-700 rounded-xl font-bold text-slate-700 dark:text-slate-200 mb-4">
                ${isDark ? '<i class="fa-solid fa-sun text-orange-500 mr-2"></i> Light Mode' : '<i class="fa-solid fa-moon text-blue-500 mr-2"></i> Dark Mode'}
            </button>
            <button id="btnAddFriend" class="w-full p-4 bg-blue-50 dark:bg-blue-900/30 text-blue-600 dark:text-blue-400 rounded-xl font-bold mb-4">Add Friend</button>
        </div>
    `;
    view.openModal(html);
    
    document.getElementById('btnTheme').onclick = () => {
        const newTheme = app.toggleTheme();
        view.applyTheme(newTheme);
        view.closeModal(); // Close to refresh UI text
    };

    document.getElementById('btnAddFriend').onclick = () => {
        const n = prompt("Friend Name:");
        if(n) { app.addPerson(n); view.closeModal(); view.renderDashboard(app.calculateTotals()); }
    };
}