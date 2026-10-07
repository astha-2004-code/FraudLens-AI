import React from 'react';
import { Search, Filter, AlertTriangle, ShieldCheck, Clock, TrendingUp } from 'lucide-react';
import { AreaChart, Area, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, BarChart, Bar, PieChart, Pie, Cell } from 'recharts';

const dataOverTime = [
  { name: 'Mon', count: 12 },
  { name: 'Tue', count: 19 },
  { name: 'Wed', count: 15 },
  { name: 'Thu', count: 25 },
  { name: 'Fri', count: 22 },
  { name: 'Sat', count: 30 },
  { name: 'Sun', count: 14 },
];

const riskData = [
  { name: 'Low', value: 400 },
  { name: 'Medium', value: 300 },
  { name: 'High', value: 200 },
  { name: 'Critical', value: 100 },
];

const COLORS = ['#3b82f6', '#f59e0b', '#ef4444', '#7f1d1d'];

const mockInvestigations = [
  { id: 'INV-1029', tx: 'TX-99812', customer: 'Alice Smith', amount: '₹42,000', score: 85, level: 'CRITICAL', status: 'PENDING', date: '2023-10-27' },
  { id: 'INV-1030', tx: 'TX-99813', customer: 'Bob Jones', amount: '₹12,500', score: 65, level: 'HIGH', status: 'OPEN', date: '2023-10-27' },
  { id: 'INV-1031', tx: 'TX-99814', customer: 'Charlie Day', amount: '₹8,200', score: 45, level: 'MEDIUM', status: 'CLOSED', date: '2023-10-26' },
  { id: 'INV-1032', tx: 'TX-99815', customer: 'Diana Ross', amount: '₹95,000', score: 92, level: 'CRITICAL', status: 'PENDING', date: '2023-10-26' },
];

const Dashboard = () => {
  return (
    <div className="flex-1 bg-slate-950 h-screen overflow-y-auto text-slate-200">
      <div className="p-8">
        <header className="mb-8 flex justify-between items-center">
          <div>
            <h1 className="text-3xl font-bold text-slate-100">Overview</h1>
            <p className="text-slate-400 mt-1">Monitor investigations and risk signals</p>
          </div>
          <div className="flex space-x-4">
            <div className="relative">
              <Search className="absolute left-3 top-1/2 -translate-y-1/2 text-slate-500" size={18} />
              <input 
                type="text" 
                placeholder="Search cases..." 
                className="pl-10 pr-4 py-2 bg-slate-900 border border-slate-800 rounded-lg focus:outline-none focus:border-blue-500 focus:ring-1 focus:ring-blue-500 transition-all text-sm w-64"
              />
            </div>
            <button className="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-lg text-sm font-medium transition-colors shadow-lg shadow-blue-900/20">
              Generate Report
            </button>
          </div>
        </header>

        {/* Stats Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
          {[
            { label: 'Total Investigations', value: '1,284', icon: <Search className="text-blue-400" />, trend: '+12%' },
            { label: 'Critical Risk', value: '142', icon: <AlertTriangle className="text-rose-500" />, trend: '+5%' },
            { label: 'Pending Review', value: '56', icon: <Clock className="text-amber-400" />, trend: '-2%' },
            { label: 'Avg Resolution Time', value: '2.4h', icon: <TrendingUp className="text-emerald-400" />, trend: '-15%' },
          ].map((stat, i) => (
            <div key={i} className="bg-slate-900 border border-slate-800 p-6 rounded-2xl shadow-sm">
              <div className="flex justify-between items-start mb-4">
                <div className="p-3 bg-slate-800/50 rounded-xl">{stat.icon}</div>
                <span className={`text-xs font-semibold px-2 py-1 rounded-full ${stat.trend.startsWith('+') ? 'bg-rose-500/10 text-rose-400' : 'bg-emerald-500/10 text-emerald-400'}`}>
                  {stat.trend}
                </span>
              </div>
              <h3 className="text-slate-400 text-sm font-medium mb-1">{stat.label}</h3>
              <p className="text-3xl font-bold text-slate-100">{stat.value}</p>
            </div>
          ))}
        </div>

        {/* Charts Section */}
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6 mb-8">
          <div className="bg-slate-900 border border-slate-800 p-6 rounded-2xl lg:col-span-2">
            <h3 className="text-lg font-bold mb-6 text-slate-100">Investigations Over Time</h3>
            <div className="h-72">
              <ResponsiveContainer width="100%" height="100%">
                <AreaChart data={dataOverTime}>
                  <defs>
                    <linearGradient id="colorCount" x1="0" y1="0" x2="0" y2="1">
                      <stop offset="5%" stopColor="#3b82f6" stopOpacity={0.3}/>
                      <stop offset="95%" stopColor="#3b82f6" stopOpacity={0}/>
                    </linearGradient>
                  </defs>
                  <CartesianGrid strokeDasharray="3 3" stroke="#1e293b" vertical={false} />
                  <XAxis dataKey="name" stroke="#64748b" tickLine={false} axisLine={false} />
                  <YAxis stroke="#64748b" tickLine={false} axisLine={false} />
                  <Tooltip contentStyle={{ backgroundColor: '#0f172a', borderColor: '#1e293b', borderRadius: '8px' }} />
                  <Area type="monotone" dataKey="count" stroke="#3b82f6" strokeWidth={3} fillOpacity={1} fill="url(#colorCount)" />
                </AreaChart>
              </ResponsiveContainer>
            </div>
          </div>
          
          <div className="bg-slate-900 border border-slate-800 p-6 rounded-2xl">
            <h3 className="text-lg font-bold mb-6 text-slate-100">Risk Distribution</h3>
            <div className="h-72 flex flex-col items-center justify-center">
              <ResponsiveContainer width="100%" height="100%">
                <PieChart>
                  <Pie data={riskData} cx="50%" cy="50%" innerRadius={60} outerRadius={80} paddingAngle={5} dataKey="value">
                    {riskData.map((entry, index) => (
                      <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                    ))}
                  </Pie>
                  <Tooltip contentStyle={{ backgroundColor: '#0f172a', borderColor: '#1e293b', borderRadius: '8px' }} />
                </PieChart>
              </ResponsiveContainer>
              <div className="grid grid-cols-2 gap-4 mt-4 w-full">
                {riskData.map((d, i) => (
                  <div key={i} className="flex items-center text-sm">
                    <div className="w-3 h-3 rounded-full mr-2" style={{ backgroundColor: COLORS[i] }}></div>
                    <span className="text-slate-400">{d.name}</span>
                  </div>
                ))}
              </div>
            </div>
          </div>
        </div>

        {/* Recent Investigations Table */}
        <div className="bg-slate-900 border border-slate-800 rounded-2xl overflow-hidden">
          <div className="p-6 border-b border-slate-800 flex justify-between items-center bg-slate-900/50">
            <h3 className="text-lg font-bold text-slate-100">Recent Investigations</h3>
            <button className="flex items-center space-x-2 text-sm text-slate-400 hover:text-slate-200 transition-colors">
              <Filter size={16} />
              <span>Filter</span>
            </button>
          </div>
          <div className="overflow-x-auto">
            <table className="w-full text-left text-sm">
              <thead className="bg-slate-800/50 text-slate-400">
                <tr>
                  <th className="px-6 py-4 font-medium">Case ID</th>
                  <th className="px-6 py-4 font-medium">Customer</th>
                  <th className="px-6 py-4 font-medium">Amount</th>
                  <th className="px-6 py-4 font-medium">Risk Score</th>
                  <th className="px-6 py-4 font-medium">Level</th>
                  <th className="px-6 py-4 font-medium">Status</th>
                  <th className="px-6 py-4 font-medium">Date</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-800">
                {mockInvestigations.map((inv, idx) => (
                  <tr key={idx} className="hover:bg-slate-800/30 transition-colors cursor-pointer">
                    <td className="px-6 py-4 font-medium text-blue-400">{inv.id}</td>
                    <td className="px-6 py-4">
                      <div className="flex flex-col">
                        <span className="text-slate-200">{inv.customer}</span>
                        <span className="text-slate-500 text-xs">{inv.tx}</span>
                      </div>
                    </td>
                    <td className="px-6 py-4 font-medium">{inv.amount}</td>
                    <td className="px-6 py-4">
                      <div className="flex items-center space-x-2">
                        <div className="w-full bg-slate-800 rounded-full h-1.5 max-w-[60px]">
                          <div className={`h-1.5 rounded-full ${inv.score > 80 ? 'bg-rose-500' : inv.score > 60 ? 'bg-amber-500' : 'bg-blue-500'}`} style={{ width: `${inv.score}%` }}></div>
                        </div>
                        <span>{inv.score}</span>
                      </div>
                    </td>
                    <td className="px-6 py-4">
                      <span className={`px-2.5 py-1 text-xs font-semibold rounded-md ${
                        inv.level === 'CRITICAL' ? 'bg-rose-500/10 text-rose-500 border border-rose-500/20' : 
                        inv.level === 'HIGH' ? 'bg-amber-500/10 text-amber-500 border border-amber-500/20' :
                        'bg-blue-500/10 text-blue-400 border border-blue-500/20'
                      }`}>
                        {inv.level}
                      </span>
                    </td>
                    <td className="px-6 py-4">
                      <div className="flex items-center space-x-2">
                        <div className={`w-2 h-2 rounded-full ${inv.status === 'PENDING' ? 'bg-amber-400' : inv.status === 'OPEN' ? 'bg-blue-400' : 'bg-emerald-400'}`}></div>
                        <span className="text-slate-300">{inv.status}</span>
                      </div>
                    </td>
                    <td className="px-6 py-4 text-slate-400">{inv.date}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
          <div className="p-4 border-t border-slate-800 flex justify-center">
            <button className="text-sm text-blue-400 hover:text-blue-300 font-medium">View All Investigations</button>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Dashboard;
