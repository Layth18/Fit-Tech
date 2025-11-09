import React, { useState } from 'react';
import { 
  TrendingUp, LogOut, Bell, FileText, Download, Eye, 
  Check, Users, Trophy, GitCompare, Calendar, Target,
  Activity, Award, BarChart3, PieChart, Image, X
} from 'lucide-react';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, LineChart, Line } from 'recharts';

const ReportGenerationPage = () => {
  const [user] = useState({ name: 'Demo User', email: 'demo@sports.com' });
  const [reportType, setReportType] = useState('player');
  const [selectedPlayer, setSelectedPlayer] = useState('John Doe');
  const [selectedMatch, setSelectedMatch] = useState('Blue Thunder FC - May 5, 2025');
  const [selectedComparison, setSelectedComparison] = useState('John Doe vs Mike Smith');
  const [isGenerating, setIsGenerating] = useState(false);
  const [showToast, setShowToast] = useState(false);
  const [showPreview, setShowPreview] = useState(true);
  
  const [includeStats, setIncludeStats] = useState({
    summary: true,
    performance: true,
    charts: true,
    timeline: false,
    heatmap: false,
    comparison: false
  });

  const players = ['John Doe', 'Mike Smith', 'Tom Brown', 'Alex Johnson'];
  const matches = ['Blue Thunder FC - May 5, 2025', 'Red Dragons - Apr 28, 2025', 'Silver Knights - Apr 21, 2025'];
  const comparisons = ['John Doe vs Mike Smith', 'Current Team vs Blue Thunder FC', 'Tom Brown vs Chris Lee'];

  const performanceData = [
    { month: 'Jan', goals: 3, assists: 2 },
    { month: 'Feb', goals: 4, assists: 1 },
    { month: 'Mar', goals: 5, assists: 2 },
    { month: 'Apr', goals: 4, assists: 1 },
    { month: 'May', goals: 2, assists: 1 },
  ];

  const handleLogout = () => {
    localStorage.removeItem('keycloak_token');
    localStorage.removeItem('user_name');
    window.location.href = '/login';
  };

  const handleGenerateReport = () => {
    setIsGenerating(true);
    setShowToast(true);

    // Simulate PDF generation
    setTimeout(() => {
      setIsGenerating(false);
      setShowToast(false);
      
      // Show success message
      const successToast = document.createElement('div');
      successToast.className = 'fixed top-20 right-4 bg-green-600 text-white px-6 py-4 rounded-lg shadow-2xl flex items-center space-x-3 z-50 animate-slide-in';
      successToast.innerHTML = `
        <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"></path>
        </svg>
        <span class="font-semibold">Report generated successfully!</span>
      `;
      document.body.appendChild(successToast);
      
      setTimeout(() => {
        successToast.remove();
      }, 3000);
    }, 3000);
  };

  const toggleStat = (stat) => {
    setIncludeStats({ ...includeStats, [stat]: !includeStats[stat] });
  };

  const getReportTitle = () => {
    switch (reportType) {
      case 'player': return `Player Report - ${selectedPlayer}`;
      case 'match': return `Match Report - ${selectedMatch}`;
      case 'comparison': return `Comparison Report - ${selectedComparison}`;
      default: return 'Performance Report';
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-slate-800 to-slate-900">
      <style>{`
        @keyframes slide-in {
          from {
            transform: translateX(100%);
            opacity: 0;
          }
          to {
            transform: translateX(0);
            opacity: 1;
          }
        }
        
        @keyframes bounce-small {
          0%, 100% {
            transform: translateY(0);
          }
          50% {
            transform: translateY(-10px);
          }
        }
        
        .animate-slide-in {
          animation: slide-in 0.3s ease-out;
        }
        
        .bounce-small {
          animation: bounce-small 0.6s infinite;
        }
      `}</style>

      

      {/* Toast Notification */}
      {showToast && (
        <div className="fixed top-20 right-4 bg-slate-800 border border-slate-700 text-white px-6 py-4 rounded-lg shadow-2xl flex items-center space-x-3 z-50 animate-slide-in">
          <div className="w-8 h-8 relative">
            <div className="w-6 h-6 bg-gradient-to-br from-blue-600 to-blue-800 rounded-full bounce-small absolute top-1 left-1"></div>
          </div>
          <span className="font-semibold">Generating report...</span>
        </div>
      )}

      {/* Main Content */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Header */}
        <div className="mb-8">
          <h2 className="text-3xl font-bold text-white mb-2">Generate Analytics Report</h2>
          <p className="text-slate-400">Create custom reports with selected statistics and visualizations</p>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          {/* Left Panel - Configuration */}
          <div className="lg:col-span-1 space-y-6">
            {/* Report Type Selection */}
            <div className="bg-gradient-to-br from-slate-800 to-slate-900 rounded-2xl p-6 border border-slate-700/50 shadow-xl">
              <h3 className="text-lg font-semibold text-blue-400 mb-4 flex items-center space-x-2">
                <FileText className="w-5 h-5" />
                <span>Report Type</span>
              </h3>
              
              <div className="space-y-3">
                <button
                  onClick={() => setReportType('player')}
                  className={`w-full flex items-center space-x-3 p-4 rounded-lg border-2 transition-all ${
                    reportType === 'player'
                      ? 'border-blue-600 bg-blue-600/20'
                      : 'border-slate-700 hover:border-slate-600 bg-slate-800/50'
                  }`}
                >
                  <div className={`w-10 h-10 rounded-lg flex items-center justify-center ${
                    reportType === 'player' ? 'bg-blue-600/30' : 'bg-slate-700'
                  }`}>
                    <Users className={`w-5 h-5 ${reportType === 'player' ? 'text-blue-400' : 'text-slate-400'}`} />
                  </div>
                  <div className="flex-1 text-left">
                    <p className="text-white font-semibold">Player Report</p>
                    <p className="text-slate-400 text-xs">Individual player statistics</p>
                  </div>
                  {reportType === 'player' && <Check className="w-5 h-5 text-blue-400" />}
                </button>

                <button
                  onClick={() => setReportType('match')}
                  className={`w-full flex items-center space-x-3 p-4 rounded-lg border-2 transition-all ${
                    reportType === 'match'
                      ? 'border-blue-600 bg-blue-600/20'
                      : 'border-slate-700 hover:border-slate-600 bg-slate-800/50'
                  }`}
                >
                  <div className={`w-10 h-10 rounded-lg flex items-center justify-center ${
                    reportType === 'match' ? 'bg-blue-600/30' : 'bg-slate-700'
                  }`}>
                    <Trophy className={`w-5 h-5 ${reportType === 'match' ? 'text-blue-400' : 'text-slate-400'}`} />
                  </div>
                  <div className="flex-1 text-left">
                    <p className="text-white font-semibold">Match Report</p>
                    <p className="text-slate-400 text-xs">Game analysis and stats</p>
                  </div>
                  {reportType === 'match' && <Check className="w-5 h-5 text-blue-400" />}
                </button>

                <button
                  onClick={() => setReportType('comparison')}
                  className={`w-full flex items-center space-x-3 p-4 rounded-lg border-2 transition-all ${
                    reportType === 'comparison'
                      ? 'border-blue-600 bg-blue-600/20'
                      : 'border-slate-700 hover:border-slate-600 bg-slate-800/50'
                  }`}
                >
                  <div className={`w-10 h-10 rounded-lg flex items-center justify-center ${
                    reportType === 'comparison' ? 'bg-blue-600/30' : 'bg-slate-700'
                  }`}>
                    <GitCompare className={`w-5 h-5 ${reportType === 'comparison' ? 'text-blue-400' : 'text-slate-400'}`} />
                  </div>
                  <div className="flex-1 text-left">
                    <p className="text-white font-semibold">Comparison Report</p>
                    <p className="text-slate-400 text-xs">Side-by-side analysis</p>
                  </div>
                  {reportType === 'comparison' && <Check className="w-5 h-5 text-blue-400" />}
                </button>
              </div>
            </div>

            {/* Subject Selection */}
            <div className="bg-gradient-to-br from-slate-800 to-slate-900 rounded-2xl p-6 border border-slate-700/50 shadow-xl">
              <h3 className="text-lg font-semibold text-blue-400 mb-4">Select Subject</h3>
              
              {reportType === 'player' && (
                <select
                  value={selectedPlayer}
                  onChange={(e) => setSelectedPlayer(e.target.value)}
                  className="w-full bg-slate-700/50 border border-slate-600 rounded-lg px-4 py-3 text-white focus:outline-none focus:ring-2 focus:ring-blue-600"
                >
                  {players.map(player => (
                    <option key={player} value={player}>{player}</option>
                  ))}
                </select>
              )}

              {reportType === 'match' && (
                <select
                  value={selectedMatch}
                  onChange={(e) => setSelectedMatch(e.target.value)}
                  className="w-full bg-slate-700/50 border border-slate-600 rounded-lg px-4 py-3 text-white focus:outline-none focus:ring-2 focus:ring-blue-600"
                >
                  {matches.map(match => (
                    <option key={match} value={match}>{match}</option>
                  ))}
                </select>
              )}

              {reportType === 'comparison' && (
                <select
                  value={selectedComparison}
                  onChange={(e) => setSelectedComparison(e.target.value)}
                  className="w-full bg-slate-700/50 border border-slate-600 rounded-lg px-4 py-3 text-white focus:outline-none focus:ring-2 focus:ring-blue-600"
                >
                  {comparisons.map(comp => (
                    <option key={comp} value={comp}>{comp}</option>
                  ))}
                </select>
              )}
            </div>

            {/* Include Options */}
            <div className="bg-gradient-to-br from-slate-800 to-slate-900 rounded-2xl p-6 border border-slate-700/50 shadow-xl">
              <h3 className="text-lg font-semibold text-blue-400 mb-4">Include in Report</h3>
              
              <div className="space-y-2">
                {Object.entries({
                  summary: { label: 'Summary Statistics', icon: BarChart3 },
                  performance: { label: 'Performance Metrics', icon: Activity },
                  charts: { label: 'Charts & Graphs', icon: PieChart },
                  timeline: { label: 'Timeline View', icon: Calendar },
                  heatmap: { label: 'Heat Maps', icon: Target },
                  comparison: { label: 'Comparison Data', icon: GitCompare }
                }).map(([key, { label, icon: Icon }]) => (
                  <label
                    key={key}
                    className="flex items-center space-x-3 p-3 rounded-lg hover:bg-slate-800/50 cursor-pointer transition-colors"
                  >
                    <input
                      type="checkbox"
                      checked={includeStats[key]}
                      onChange={() => toggleStat(key)}
                      className="w-5 h-5 rounded border-slate-600 text-blue-600 focus:ring-2 focus:ring-blue-600 focus:ring-offset-0 bg-slate-700"
                    />
                    <Icon className="w-5 h-5 text-slate-400" />
                    <span className="text-white flex-1">{label}</span>
                  </label>
                ))}
              </div>
            </div>

            {/* Action Buttons */}
            <div className="space-y-3">
              <button
                onClick={() => setShowPreview(!showPreview)}
                className="w-full flex items-center justify-center space-x-2 px-6 py-3 bg-slate-700/50 hover:bg-slate-700 text-white rounded-lg transition-colors"
              >
                <Eye className="w-5 h-5" />
                <span className="font-semibold">{showPreview ? 'Hide' : 'Show'} Preview</span>
              </button>

              <button
                onClick={handleGenerateReport}
                disabled={isGenerating}
                className="w-full flex items-center justify-center space-x-2 px-6 py-4 bg-gradient-to-r from-blue-600 to-blue-700 hover:from-blue-700 hover:to-blue-800 text-white rounded-lg transition-all shadow-lg hover:shadow-xl disabled:opacity-50 disabled:cursor-not-allowed"
              >
                {isGenerating ? (
                  <>
                    <div className="w-5 h-5 border-2 border-white border-t-transparent rounded-full animate-spin"></div>
                    <span className="font-semibold">Generating...</span>
                  </>
                ) : (
                  <>
                    <Download className="w-5 h-5" />
                    <span className="font-semibold">Generate PDF Report</span>
                  </>
                )}
              </button>
            </div>
          </div>

          {/* Right Panel - Live Preview */}
          {showPreview && (
            <div className="lg:col-span-2">
              <div className="bg-gradient-to-br from-slate-300 via-slate-200 to-slate-300 rounded-2xl p-8 border border-slate-400/50 shadow-2xl">
                {/* Report Header */}
                <div className="bg-white rounded-xl p-6 mb-6 border border-slate-300">
                  <div className="flex items-start justify-between mb-4">
                    <div>
                      <h2 className="text-2xl font-bold text-slate-900 mb-2">{getReportTitle()}</h2>
                      <p className="text-slate-600 text-sm">
                        Generated on {new Date().toLocaleDateString('en-US', { month: 'long', day: 'numeric', year: 'numeric' })}
                      </p>
                    </div>
                    <div className="w-12 h-12 bg-gradient-to-br from-blue-600 to-blue-800 rounded-lg flex items-center justify-center">
                      <TrendingUp className="w-6 h-6 text-white" />
                    </div>
                  </div>
                  <div className="h-1 bg-gradient-to-r from-blue-600 to-slate-400 rounded-full"></div>
                </div>

                {/* Report Content */}
                <div className="space-y-4">
                  {includeStats.summary && (
                    <div className="bg-white rounded-xl p-6 border border-slate-300">
                      <h3 className="text-lg font-bold text-blue-600 mb-4 flex items-center space-x-2">
                        <BarChart3 className="w-5 h-5" />
                        <span>Summary Statistics</span>
                      </h3>
                      <div className="grid grid-cols-3 gap-4">
                        <div className="text-center p-4 bg-slate-50 rounded-lg border border-slate-200">
                          <p className="text-slate-600 text-sm mb-1">Goals</p>
                          <p className="text-3xl font-bold text-blue-600">18</p>
                        </div>
                        <div className="text-center p-4 bg-slate-50 rounded-lg border border-slate-200">
                          <p className="text-slate-600 text-sm mb-1">Assists</p>
                          <p className="text-3xl font-bold text-blue-600">7</p>
                        </div>
                        <div className="text-center p-4 bg-slate-50 rounded-lg border border-slate-200">
                          <p className="text-slate-600 text-sm mb-1">Rating</p>
                          <p className="text-3xl font-bold text-yellow-500">8.9</p>
                        </div>
                      </div>
                    </div>
                  )}

                  {includeStats.performance && (
                    <div className="bg-white rounded-xl p-6 border border-slate-300">
                      <h3 className="text-lg font-bold text-blue-600 mb-4 flex items-center space-x-2">
                        <Activity className="w-5 h-5" />
                        <span>Performance Metrics</span>
                      </h3>
                      <div className="space-y-3">
                        <div>
                          <div className="flex justify-between mb-2">
                            <span className="text-slate-700 text-sm">Shot Accuracy</span>
                            <span className="text-slate-900 font-semibold">78%</span>
                          </div>
                          <div className="w-full bg-slate-200 rounded-full h-2">
                            <div className="bg-gradient-to-r from-blue-600 to-blue-400 h-2 rounded-full" style={{ width: '78%' }}></div>
                          </div>
                        </div>
                        <div>
                          <div className="flex justify-between mb-2">
                            <span className="text-slate-700 text-sm">Pass Completion</span>
                            <span className="text-slate-900 font-semibold">84%</span>
                          </div>
                          <div className="w-full bg-slate-200 rounded-full h-2">
                            <div className="bg-gradient-to-r from-blue-600 to-blue-400 h-2 rounded-full" style={{ width: '84%' }}></div>
                          </div>
                        </div>
                      </div>
                    </div>
                  )}

                  {includeStats.charts && (
                    <div className="bg-white rounded-xl p-6 border border-slate-300">
                      <h3 className="text-lg font-bold text-blue-600 mb-4 flex items-center space-x-2">
                        <PieChart className="w-5 h-5" />
                        <span>Performance Chart</span>
                      </h3>
                      <ResponsiveContainer width="100%" height={200}>
                        <BarChart data={performanceData}>
                          <CartesianGrid strokeDasharray="3 3" stroke="#e2e8f0" />
                          <XAxis dataKey="month" stroke="#64748b" />
                          <YAxis stroke="#64748b" />
                          <Tooltip 
                            contentStyle={{ backgroundColor: '#ffffff', border: '1px solid #cbd5e1', borderRadius: '8px' }}
                          />
                          <Bar dataKey="goals" fill="#3b82f6" radius={[8, 8, 0, 0]} />
                          <Bar dataKey="assists" fill="#94a3b8" radius={[8, 8, 0, 0]} />
                        </BarChart>
                      </ResponsiveContainer>
                    </div>
                  )}

                  {includeStats.timeline && (
                    <div className="bg-white rounded-xl p-6 border border-slate-300">
                      <h3 className="text-lg font-bold text-blue-600 mb-4 flex items-center space-x-2">
                        <Calendar className="w-5 h-5" />
                        <span>Timeline View</span>
                      </h3>
                      <div className="space-y-3">
                        {['May 5 - Victory vs Blue Thunder', 'Apr 28 - Draw vs Red Dragons', 'Apr 21 - Victory vs Silver Knights'].map((event, i) => (
                          <div key={i} className="flex items-center space-x-3 p-3 bg-slate-50 rounded-lg border border-slate-200">
                            <div className="w-2 h-2 bg-blue-600 rounded-full"></div>
                            <span className="text-slate-700 text-sm">{event}</span>
                          </div>
                        ))}
                      </div>
                    </div>
                  )}

                  {includeStats.heatmap && (
                    <div className="bg-white rounded-xl p-6 border border-slate-300">
                      <h3 className="text-lg font-bold text-blue-600 mb-4 flex items-center space-x-2">
                        <Target className="w-5 h-5" />
                        <span>Heat Map</span>
                      </h3>
                      <div className="aspect-video bg-slate-100 rounded-lg flex items-center justify-center border-2 border-dashed border-slate-300">
                        <div className="text-center">
                          <Image className="w-12 h-12 text-slate-400 mx-auto mb-2" />
                          <p className="text-slate-500 text-sm">Heat map visualization</p>
                        </div>
                      </div>
                    </div>
                  )}

                  {includeStats.comparison && (
                    <div className="bg-white rounded-xl p-6 border border-slate-300">
                      <h3 className="text-lg font-bold text-blue-600 mb-4 flex items-center space-x-2">
                        <GitCompare className="w-5 h-5" />
                        <span>Comparison Data</span>
                      </h3>
                      <table className="w-full">
                        <thead>
                          <tr className="border-b-2 border-slate-200">
                            <th className="text-left py-2 text-slate-700 text-sm">Metric</th>
                            <th className="text-center py-2 text-slate-700 text-sm">Player 1</th>
                            <th className="text-center py-2 text-slate-700 text-sm">Player 2</th>
                          </tr>
                        </thead>
                        <tbody>
                          <tr className="border-b border-slate-100">
                            <td className="py-2 text-slate-600 text-sm">Goals</td>
                            <td className="text-center py-2 text-slate-900 font-semibold">18</td>
                            <td className="text-center py-2 text-slate-900 font-semibold">6</td>
                          </tr>
                          <tr className="border-b border-slate-100">
                            <td className="py-2 text-slate-600 text-sm">Assists</td>
                            <td className="text-center py-2 text-slate-900 font-semibold">7</td>
                            <td className="text-center py-2 text-slate-900 font-semibold">12</td>
                          </tr>
                        </tbody>
                      </table>
                    </div>
                  )}
                </div>

                {/* Report Footer */}
                <div className="bg-white rounded-xl p-4 mt-6 border border-slate-300">
                  <p className="text-slate-500 text-xs text-center">
                    Sports Analytics Platform • Generated by {user.name} • © 2025 All rights reserved
                  </p>
                </div>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default ReportGenerationPage;