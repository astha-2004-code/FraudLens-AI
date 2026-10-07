import React, { useState } from 'react';
import { ShieldAlert, Info, Activity, Clock, ShieldCheck, MapPin, Monitor, CheckCircle, XCircle } from 'lucide-react';

const mockInvestigation = {
  id: 'INV-1029',
  tx: 'TX-99812',
  customer: 'Alice Smith',
  amount: '₹42,000',
  score: 85,
  level: 'CRITICAL',
  status: 'PENDING',
  date: '2023-10-27',
  hypothesis: 'The transaction is highly unusual for the customer, originating from a new device in a different country (Russia) within 4 hours of a local transaction.',
  signals: [
    { type: 'AMOUNT_ANOMALY', impact: 20 },
    { type: 'NEW_DEVICE', impact: 15 },
    { type: 'IMPOSSIBLE_TRAVEL', impact: 20 },
    { type: 'VELOCITY_ANOMALY', impact: 20 },
  ],
  evidence: {
    supporting: ['Customer average transaction is ₹4,200', 'New iPhone 15 device detected', 'Transaction originated from IP in Moscow'],
    contradicting: ['Customer previously traveled to Moscow in 2021', 'Merchant is somewhat related to previous travel expenses'],
  }
};

const InvestigationDetail = () => {
  const [activeTab, setActiveTab] = useState('overview');

  return (
    <div className="flex-1 bg-slate-950 h-screen overflow-y-auto text-slate-200">
      <div className="p-8 max-w-7xl mx-auto">
        <header className="mb-8 flex justify-between items-start">
          <div>
            <div className="flex items-center space-x-3 mb-2">
              <h1 className="text-3xl font-bold text-slate-100">{mockInvestigation.id}</h1>
              <span className="px-3 py-1 bg-rose-500/10 text-rose-500 border border-rose-500/20 rounded-md text-sm font-semibold">
                {mockInvestigation.level} RISK ({mockInvestigation.score}/100)
              </span>
            </div>
            <p className="text-slate-400">Transaction {mockInvestigation.tx} by {mockInvestigation.customer}</p>
          </div>
          <div className="flex space-x-3">
            <button className="bg-slate-800 hover:bg-slate-700 text-slate-200 px-4 py-2 rounded-lg text-sm font-medium transition-colors border border-slate-700">
              View Evidence
            </button>
            <button className="bg-slate-800 hover:bg-slate-700 text-slate-200 px-4 py-2 rounded-lg text-sm font-medium transition-colors border border-slate-700">
              Find Similar Cases
            </button>
            <button className="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-lg text-sm font-medium transition-colors shadow-lg shadow-blue-900/20 flex items-center space-x-2">
              <ShieldAlert size={16} />
              <span>Challenge Assessment</span>
            </button>
            <button className="bg-emerald-600 hover:bg-emerald-700 text-white px-4 py-2 rounded-lg text-sm font-medium transition-colors shadow-lg shadow-emerald-900/20">
              Investigate
            </button>
          </div>
        </header>

        <div className="flex space-x-1 mb-8 border-b border-slate-800">
          {['overview', 'timeline', 'customer', 'evidence', 'graph', 'policies'].map(tab => (
            <button 
              key={tab}
              onClick={() => setActiveTab(tab)}
              className={`px-6 py-3 text-sm font-medium capitalize border-b-2 transition-colors ${activeTab === tab ? 'border-blue-500 text-blue-400' : 'border-transparent text-slate-400 hover:text-slate-200 hover:border-slate-700'}`}
            >
              {tab}
            </button>
          ))}
        </div>

        {activeTab === 'overview' && (
          <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
            <div className="lg:col-span-2 space-y-6">
              <div className="bg-slate-900 border border-slate-800 p-6 rounded-2xl shadow-sm">
                <h3 className="text-lg font-bold mb-4 text-slate-100 flex items-center">
                  <Activity className="mr-2 text-blue-400" size={20} />
                  AI Assessment
                </h3>
                <p className="text-slate-300 leading-relaxed mb-6">
                  {mockInvestigation.hypothesis}
                </p>
                <div className="bg-slate-950 p-4 rounded-xl border border-slate-800">
                  <h4 className="text-sm font-semibold text-slate-400 mb-3 uppercase tracking-wider">Recommended Next Steps</h4>
                  <ul className="space-y-2">
                    <li className="flex items-start"><span className="text-blue-400 mr-2">•</span> Contact customer to verify recent travel to Russia.</li>
                    <li className="flex items-start"><span className="text-blue-400 mr-2">•</span> Review transaction velocity on the new device.</li>
                    <li className="flex items-start"><span className="text-blue-400 mr-2">•</span> Temporarily freeze outbound transfers until verified.</li>
                  </ul>
                </div>
              </div>

              <div className="bg-slate-900 border border-slate-800 p-6 rounded-2xl shadow-sm">
                <h3 className="text-lg font-bold mb-4 text-slate-100 flex items-center">
                  <Info className="mr-2 text-blue-400" size={20} />
                  Risk Signals
                </h3>
                <div className="space-y-3">
                  {mockInvestigation.signals.map((sig, i) => (
                    <div key={i} className="flex justify-between items-center p-3 bg-slate-800/50 rounded-xl border border-slate-700/50">
                      <span className="font-medium text-slate-300">{sig.type.replace('_', ' ')}</span>
                      <span className="text-rose-400 font-bold">+{sig.impact} pts</span>
                    </div>
                  ))}
                </div>
              </div>
            </div>

            <div className="space-y-6">
              <div className="bg-slate-900 border border-slate-800 p-6 rounded-2xl shadow-sm">
                <h3 className="text-lg font-bold mb-4 text-slate-100 flex items-center">
                  <ShieldCheck className="mr-2 text-emerald-400" size={20} />
                  Evidence Summary
                </h3>
                <div className="mb-6">
                  <h4 className="text-sm font-semibold text-emerald-400 mb-2 flex items-center">
                    <CheckCircle size={16} className="mr-1" /> Supporting
                  </h4>
                  <ul className="space-y-2 text-sm text-slate-300">
                    {mockInvestigation.evidence.supporting.map((ev, i) => (
                      <li key={i} className="flex items-start"><span className="text-slate-500 mr-2">-</span> {ev}</li>
                    ))}
                  </ul>
                </div>
                <div>
                  <h4 className="text-sm font-semibold text-amber-400 mb-2 flex items-center">
                    <XCircle size={16} className="mr-1" /> Contradicting
                  </h4>
                  <ul className="space-y-2 text-sm text-slate-300">
                    {mockInvestigation.evidence.contradicting.map((ev, i) => (
                      <li key={i} className="flex items-start"><span className="text-slate-500 mr-2">-</span> {ev}</li>
                    ))}
                  </ul>
                </div>
              </div>

              <div className="bg-slate-900 border border-slate-800 p-6 rounded-2xl shadow-sm">
                 <h3 className="text-lg font-bold mb-4 text-slate-100">Case Information</h3>
                 <div className="space-y-4 text-sm">
                    <div className="flex justify-between">
                      <span className="text-slate-400">Amount</span>
                      <span className="font-medium text-slate-200">{mockInvestigation.amount}</span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-slate-400">Customer</span>
                      <span className="font-medium text-slate-200">{mockInvestigation.customer}</span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-slate-400">Date</span>
                      <span className="font-medium text-slate-200">{mockInvestigation.date}</span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-slate-400">Status</span>
                      <span className="font-medium text-amber-400">{mockInvestigation.status}</span>
                    </div>
                 </div>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default InvestigationDetail;
