export class SplitifyModel {
    constructor() {
        this.STORAGE_KEY = 'splitify_v9';
        this.data = {
            cash: 0,
            bank: 0,
            week: 0,
            people: {},
            trans: [],
            tags: ['Food', 'Transport', 'Bills', 'Entertainment', 'Shopping'],
            userName: 'User',
            theme: 'light' // 'light' or 'dark'
        };
        this.loadData();
    }

    loadData() {
        const saved = localStorage.getItem(this.STORAGE_KEY);
        if (saved) {
            this.data = JSON.parse(saved);
        } else {
            // Migration check (optional) or Defaults
            const old = localStorage.getItem('splitifyData_v8');
            if(old) this.data = { ...this.data, ...JSON.parse(old) };
        }
    }

    saveData() {
        localStorage.setItem(this.STORAGE_KEY, JSON.stringify(this.data));
    }

    calculateTotals() {
        let c = 0, b = 0, w = 0;
        let pBal = {};
        for (let k in this.data.people) pBal[k] = 0;

        this.data.trans.forEach(t => {
            const amt = parseInt(t.amt) || 0;
            const p = t.person;
            const isBank = t.source === 'BANK';
            const isWeek = !t.weekReset;

            switch (t.type) {
                case 'EXPENSE':
                    if (isBank) b -= amt; else c -= amt;
                    if (isWeek) w += amt;
                    if (p && p !== 'Self' && pBal[p] !== undefined) pBal[p] += amt;
                    break;
                case 'TRANSFER_IN':
                case 'RECEIVED':
                    if (isBank) b += amt; else c += amt;
                    if (p && p !== 'Self') pBal[p] -= amt;
                    break;
                case 'TRANSFER_OUT':
                    if (isBank) b -= amt; else c -= amt;
                    if (p && p !== 'Self') pBal[p] += amt;
                    break;
                case 'SPLIT_MAIN': // Deduct Total from Wallet
                    if (isBank) b -= amt; else c -= amt;
                    break;
                case 'SPLIT_SHARE': // Track Personal Share
                    if (isWeek) w += amt;
                    break;
                case 'SPLIT_DEBIT': // Track Debt
                    if (p) pBal[p] += amt;
                    break;
                case 'BALANCE_CORRECTION':
                    if (t.mode === 'IN') { isBank ? b += amt : c += amt; }
                    else { isBank ? b -= amt : c -= amt; }
                    break;
            }
        });

        this.data.cash = c;
        this.data.bank = b;
        this.data.week = w;
        this.data.people = pBal;
        return this.data;
    }

    addTransaction(t) {
        // Pre-processing dates or tags can go here
        this.data.trans.push(t);
        this.saveData();
        return this.calculateTotals();
    }

    deleteTransaction(index) {
        this.data.trans.splice(index, 1);
        this.saveData();
    }

    addPerson(name) {
        if (!this.data.people[name]) {
            this.data.people[name] = 0;
            this.saveData();
            return true;
        }
        return false;
    }

    toggleTheme() {
        this.data.theme = this.data.theme === 'light' ? 'dark' : 'light';
        this.saveData();
        return this.data.theme;
    }

    // Logic for Unequal Splits
    calculateSplitDistribution(total, friendsList, manualAmounts) {
        // manualAmounts is object { "John": 50, "Alice": null }
        let assignedSum = 0;
        let unassignedCount = 0;
        
        // My share is implicit in the remainder usually, or explicitly set?
        // Let's assume friends + Self involved.
        // Simplified: Friends pay X, I pay remainder.
        
        friendsList.forEach(f => {
            if(manualAmounts[f]) assignedSum += manualAmounts[f];
            else unassignedCount++;
        });

        // Add Self
        if(manualAmounts['Self']) assignedSum += manualAmounts['Self'];
        else unassignedCount++;

        const remainder = total - assignedSum;
        if(remainder < 0) return { error: "Sum exceeds total!" };
        
        // If everything assigned but remainder exists -> Error (unless it's tip?)
        // If unassignedCount > 0, distribute remainder
        const autoShare = unassignedCount > 0 ? Math.round(remainder / unassignedCount) : 0;

        return {
            share: autoShare,
            remainder: remainder
        };
    }
}