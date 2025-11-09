import React, { useState } from 'react';
import { 
  TrendingUp, LogOut, Bell, Users, Shield, Target, 
  Activity, Award, ChevronDown, BarChart3, Zap, Flag
} from 'lucide-react';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer, RadarChart, PolarGrid, PolarAngleAxis, PolarRadiusAxis, Radar } from 'recharts';

const ComparisonPage = () => {
  const [user] = useState({ name: 'Demo User', email: 'demo@sports.com' });
  const [activeTab, setActiveTab] = useState('players'); // 'players' or 'teams'
  const [selectedPlayers, setSelectedPlayers] = useState(['John Doe', 'Mike Smith']);
  const [selectedTeams, setSelectedTeams] = useState(['Current Team', 'Blue Thunder FC']);

  const players = [
    { name: 'John Doe', position: 'Forward', goals: 18, assists: 7, shots: 89, passes: 456, tackles: 23, rating: 8.9, speed: 88, finishing: 92, passing: 78, defending: 45, physical: 82, dribbling: 85 },
    { name: 'Mike Smith', position: 'Midfielder', goals: 6, assists: 12, shots: 52, passes: 892, tackles: 67, rating: 8.5, speed: 76, finishing: 68, passing: 91, defending: 74, physical: 78, dribbling: 82 },
    { name: 'Tom Brown', position: 'Defender', goals: 2, assists: 3, shots: 18, passes: 678, tackles: 98, rating: 8.3, speed: 72, finishing: 45, passing: 82, defending: 94, physical: 88, dribbling: 65 },
    { name: 'Chris Lee', position: 'Forward', goals: 12, assists: 5, shots: 76, passes: 378, tackles: 19, rating: 8.7, speed: 91, finishing: 89, passing: 74, defending: 42, physical: 76, dribbling: 88 },
  ];

  const teams = [
    { name: 'Current Team', wins: 42, draws: 8, losses: 8, goalsFor: 127, goalsAgainst: 45, possession: 58, passAccuracy: 84, shotsPerGame: 16, tacklesPerGame: 22, rating: 8.6, attack: 88, midfield: 82, defense: 85, goalkeeping: 87, fitness: 84, morale: 89 },
    { name: 'Blue Thunder FC', wins: 38, draws: 12, losses: 8, goalsFor: 109, goalsAgainst: 52, possession: 54, passAccuracy: 81, shotsPerGame: 14, tacklesPerGame: 24, rating: 8.3, attack: 82, midfield: 85, defense: 80, goalkeeping: 84, fitness: 82, morale: 86 },
    { name: 'Red Dragons', wins: 35, draws: 10, losses: 13, goalsFor: 98, goalsAgainst: 58, possession: 51, passAccuracy: 79, shotsPerGame: 13, tacklesPerGame: 26, rating: 8.0, attack: 78, midfield: 79, defense: 82, goalkeeping: 81, fitness: 80, morale: 82 },
  ];

  const handleLogout = () => {
    localStorage.removeItem('keycloak_token');
    localStorage.removeItem('user_name');
    window.location.href = '/';
  };

  const getSelectedPlayerData = () => {
    return players.filter(p => selectedPlayers.includes(p.name));
  };

  const getSelectedTeamData = () => {
    return teams.filter(t => selectedTeams.includes(t.name));
  };

  // Prepare bar chart data for players
  const playerBarChartData = [
    {
      metric: 'Goals',
      ...Object.fromEntries(getSelectedPlayerData().map((p, i) => [p.name, p.goals]))
    },
    {
      metric: 'Assists',
      ...Object.fromEntries(getSelectedPlayerData().map((p, i) => [p.name, p.assists]))
    },
    {
      metric: 'Tackles',
      ...Object.fromEntries(getSelectedPlayerData().map((p, i) => [p.name, p.tackles]))
    },
  ];

  // Prepare radar chart data for players
  const playerRadarData = [
    { attribute: 'Speed', ...Object.fromEntries(getSelectedPlayerData().map(p => [p.name, p.speed])) },
    { attribute: 'Finishing', ...Object.fromEntries(getSelectedPlayerData().map(p => [p.name, p.finishing])) },
    { attribute: 'Passing', ...Object.fromEntries(getSelectedPlayerData().map(p => [p.name, p.passing])) },
    { attribute: 'Defending', ...Object.fromEntries(getSelectedPlayerData().map(p => [p.name, p.defending])) },
    { attribute: 'Physical', ...Object.fromEntries(getSelectedPlayerData().map(p => [p.name, p.physical])) },
    { attribute: 'Dribbling', ...Object.fromEntries(getSelectedPlayerData().map(p => [p.name, p.dribbling])) },
  ];

  // Prepare bar chart data for teams
  const teamBarChartData = [
    {
      metric: 'Goals For',
      ...Object.fromEntries(getSelectedTeamData().map(t => [t.name, t.goalsFor]))
    },
    {
      metric: 'Goals Against',
      ...Object.fromEntries(getSelectedTeamData().map(t => [t.name, t.goalsAgainst]))
    },
    {
      metric: 'Wins',
      ...Object.fromEntries(getSelectedTeamData().map(t => [t.name, t.wins]))
    },
  ];

  // Prepare radar chart data for teams
  const teamRadarData = [
    { attribute: 'Attack', ...Object.fromEntries(getSelectedTeamData().map(t => [t.name, t.attack])) },
    { attribute: 'Midfield', ...Object.fromEntries(getSelectedTeamData().map(t => [t.name, t.midfield])) },
    { attribute: 'Defense', ...Object.fromEntries(getSelectedTeamData().map(t => [t.name, t.defense])) },
    { attribute: 'Goalkeeping', ...Object.fromEntries(getSelectedTeamData().map(t => [t.name, t.goalkeeping])) },
    { attribute: 'Fitness', ...Object.fromEntries(getSelectedTeamData().map(t => [t.name, t.fitness])) },
    { attribute: 'Morale', ...Object.fromEntries(getSelectedTeamData().map(t => [t.name, t.morale])) },
  ];

  const colors = ['#3b82f6', '#94a3b8', '#22c55e', '#eab308', '#ef4444'];

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-slate-800 to-slate-900">

      {/* Main Content */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Header */}
        <div className="mb-8">
          <h2 className="text-3xl font-bold text-white mb-2">Performance Comparison</h2>
          <p className="text-slate-400">Analyze and compare players or teams side-by-side</p>
        </div>

        {/* Tab Switcher */}
        <div className="flex space-x-2 mb-6 bg-slate-800/50 rounded-xl p-2 w-fit">
          <button
            onClick={() => setActiveTab('players')}
            className={`flex items-center space-x-2 px-6 py-3 rounded-lg font-semibold transition-all ${
              activeTab === 'players'
                ? 'bg-gradient-to-r from-blue-600 to-blue-700 text-white shadow-lg'
                : 'text-slate-400 hover:text-white hover:bg-slate-700/50'
            }`}
          >
            <Users className="w-5 h-5" />
            <span>Player vs Player</span>
          </button>
          <button
            onClick={() => setActiveTab('teams')}
            className={`flex items-center space-x-2 px-6 py-3 rounded-lg font-semibold transition-all ${
              activeTab === 'teams'
                ? 'bg-gradient-to-r from-blue-600 to-blue-700 text-white shadow-lg'
                : 'text-slate-400 hover:text-white hover:bg-slate-700/50'
            }`}
          >
            <Shield className="w-5 h-5" />
            <span>Team vs Team</span>
          </button>
        </div>

        {/* Player vs Player Tab */}
        {activeTab === 'players' && (
          <div className="space-y-6">
            {/* Player Selection */}
            <div className="bg-gradient-to-br from-slate-800 to-slate-900 rounded-2xl p-6 border border-slate-700/50 shadow-xl">
              <h3 className="text-lg font-semibold text-blue-400 mb-4">Select Players to Compare</h3>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                {[0, 1].map((index) => (
                  <div key={index}>
                    <label className="block text-slate-400 text-sm mb-2">Player {index + 1}</label>
                    <select
                      value={selectedPlayers[index]}
                      onChange={(e) => {
                        const newSelection = [...selectedPlayers];
                        newSelection[index] = e.target.value;
                        setSelectedPlayers(newSelection);
                      }}
                      className="w-full bg-slate-700/50 border border-slate-600 rounded-lg px-4 py-3 text-white focus:outline-none focus:ring-2 focus:ring-blue-600"
                    >
                      {players.map(player => (
                        <option key={player.name} value={player.name}>
                          {player.name} - {player.position}
                        </option>
                      ))}
                    </select>
                  </div>
                ))}
              </div>
            </div>

            {/* Stats Comparison Table */}
            <div className="bg-gradient-to-br from-slate-800 to-slate-900 rounded-2xl p-6 border border-slate-700/50 shadow-xl">
              <h3 className="text-lg font-semibold text-blue-400 mb-4 flex items-center space-x-2">
                <BarChart3 className="w-5 h-5" />
                <span>Raw Statistics</span>
              </h3>
              <div className="overflow-x-auto">
                <table className="w-full">
                  <thead className="bg-slate-900/50">
                    <tr>
                      <th className="px-4 py-3 text-left text-sm font-semibold text-blue-400">Metric</th>
                      {getSelectedPlayerData().map((player, index) => (
                        <th key={index} className="px-4 py-3 text-center text-sm font-semibold text-blue-400">
                          {player.name}
                        </th>
                      ))}
                    </tr>
                  </thead>
                  <tbody className="divide-y divide-slate-700/30">
                    <tr className="hover:bg-slate-800/30">
                      <td className="px-4 py-3 text-slate-400 font-medium">Position</td>
                      {getSelectedPlayerData().map((player, index) => (
                        <td key={index} className="px-4 py-3 text-center text-white">{player.position}</td>
                      ))}
                    </tr>
                    <tr className="hover:bg-slate-800/30">
                      <td className="px-4 py-3 text-slate-400 font-medium">Goals</td>
                      {getSelectedPlayerData().map((player, index) => (
                        <td key={index} className="px-4 py-3 text-center text-green-400 font-bold text-lg">{player.goals}</td>
                      ))}
                    </tr>
                    <tr className="hover:bg-slate-800/30">
                      <td className="px-4 py-3 text-slate-400 font-medium">Assists</td>
                      {getSelectedPlayerData().map((player, index) => (
                        <td key={index} className="px-4 py-3 text-center text-blue-400 font-bold text-lg">{player.assists}</td>
                      ))}
                    </tr>
                    <tr className="hover:bg-slate-800/30">
                      <td className="px-4 py-3 text-slate-400 font-medium">Shots</td>
                      {getSelectedPlayerData().map((player, index) => (
                        <td key={index} className="px-4 py-3 text-center text-white">{player.shots}</td>
                      ))}
                    </tr>
                    <tr className="hover:bg-slate-800/30">
                      <td className="px-4 py-3 text-slate-400 font-medium">Passes</td>
                      {getSelectedPlayerData().map((player, index) => (
                        <td key={index} className="px-4 py-3 text-center text-white">{player.passes}</td>
                      ))}
                    </tr>
                    <tr className="hover:bg-slate-800/30">
                      <td className="px-4 py-3 text-slate-400 font-medium">Tackles</td>
                      {getSelectedPlayerData().map((player, index) => (
                        <td key={index} className="px-4 py-3 text-center text-white">{player.tackles}</td>
                      ))}
                    </tr>
                    <tr className="hover:bg-slate-800/30">
                      <td className="px-4 py-3 text-slate-400 font-medium">Rating</td>
                      {getSelectedPlayerData().map((player, index) => (
                        <td key={index} className="px-4 py-3 text-center">
                          <span className="px-3 py-1 bg-yellow-600/20 text-yellow-400 font-bold rounded-full">
                            {player.rating}
                          </span>
                        </td>
                      ))}
                    </tr>
                  </tbody>
                </table>
              </div>
            </div>

            {/* Bar Chart Comparison */}
            <div className="bg-gradient-to-br from-slate-800 to-slate-900 rounded-2xl p-6 border border-slate-700/50 shadow-xl">
              <h3 className="text-lg font-semibold text-blue-400 mb-6 flex items-center space-x-2">
                <Target className="w-5 h-5" />
                <span>Key Metrics Comparison</span>
              </h3>
              <ResponsiveContainer width="100%" height={300}>
                <BarChart data={playerBarChartData}>
                  <CartesianGrid strokeDasharray="3 3" stroke="#334155" />
                  <XAxis dataKey="metric" stroke="#94a3b8" />
                  <YAxis stroke="#94a3b8" />
                  <Tooltip 
                    contentStyle={{ 
                      backgroundColor: '#1e293b', 
                      border: '1px solid #475569', 
                      borderRadius: '8px' 
                    }}
                    labelStyle={{ color: '#e2e8f0' }}
                  />
                  <Legend 
                    wrapperStyle={{ paddingTop: '20px' }}
                    iconType="circle"
                  />
                  {getSelectedPlayerData().map((player, index) => (
                    <Bar 
                      key={player.name} 
                      dataKey={player.name} 
                      fill={colors[index]} 
                      radius={[8, 8, 0, 0]}
                    />
                  ))}
                </BarChart>
              </ResponsiveContainer>
            </div>

            {/* Radar Chart - Performance Fingerprint */}
            <div className="bg-gradient-to-br from-slate-800 to-slate-900 rounded-2xl p-6 border border-slate-700/50 shadow-xl">
              <h3 className="text-lg font-semibold text-blue-400 mb-6 flex items-center space-x-2">
                <Activity className="w-5 h-5" />
                <span>Performance Fingerprint</span>
              </h3>
              <ResponsiveContainer width="100%" height={400}>
                <RadarChart data={playerRadarData}>
                  <PolarGrid stroke="#475569" />
                  <PolarAngleAxis dataKey="attribute" stroke="#94a3b8" />
                  <PolarRadiusAxis angle={90} domain={[0, 100]} stroke="#94a3b8" />
                  <Tooltip 
                    contentStyle={{ 
                      backgroundColor: '#1e293b', 
                      border: '1px solid #475569', 
                      borderRadius: '8px' 
                    }}
                  />
                  <Legend 
                    wrapperStyle={{ paddingTop: '20px' }}
                    iconType="circle"
                  />
                  {getSelectedPlayerData().map((player, index) => (
                    <Radar
                      key={player.name}
                      name={player.name}
                      dataKey={player.name}
                      stroke={colors[index]}
                      fill={colors[index]}
                      fillOpacity={0.3}
                      strokeWidth={2}
                    />
                  ))}
                </RadarChart>
              </ResponsiveContainer>
            </div>
          </div>
        )}

        {/* Team vs Team Tab */}
        {activeTab === 'teams' && (
          <div className="space-y-6">
            {/* Team Selection */}
            <div className="bg-gradient-to-br from-slate-800 to-slate-900 rounded-2xl p-6 border border-slate-700/50 shadow-xl">
              <h3 className="text-lg font-semibold text-blue-400 mb-4">Select Teams to Compare</h3>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                {[0, 1].map((index) => (
                  <div key={index}>
                    <label className="block text-slate-400 text-sm mb-2">Team {index + 1}</label>
                    <select
                      value={selectedTeams[index]}
                      onChange={(e) => {
                        const newSelection = [...selectedTeams];
                        newSelection[index] = e.target.value;
                        setSelectedTeams(newSelection);
                      }}
                      className="w-full bg-slate-700/50 border border-slate-600 rounded-lg px-4 py-3 text-white focus:outline-none focus:ring-2 focus:ring-blue-600"
                    >
                      {teams.map(team => (
                        <option key={team.name} value={team.name}>
                          {team.name}
                        </option>
                      ))}
                    </select>
                  </div>
                ))}
              </div>
            </div>

            {/* Stats Comparison Table */}
            <div className="bg-gradient-to-br from-slate-800 to-slate-900 rounded-2xl p-6 border border-slate-700/50 shadow-xl">
              <h3 className="text-lg font-semibold text-blue-400 mb-4 flex items-center space-x-2">
                <BarChart3 className="w-5 h-5" />
                <span>Team Statistics</span>
              </h3>
              <div className="overflow-x-auto">
                <table className="w-full">
                  <thead className="bg-slate-900/50">
                    <tr>
                      <th className="px-4 py-3 text-left text-sm font-semibold text-blue-400">Metric</th>
                      {getSelectedTeamData().map((team, index) => (
                        <th key={index} className="px-4 py-3 text-center text-sm font-semibold text-blue-400">
                          {team.name}
                        </th>
                      ))}
                    </tr>
                  </thead>
                  <tbody className="divide-y divide-slate-700/30">
                    <tr className="hover:bg-slate-800/30">
                      <td className="px-4 py-3 text-slate-400 font-medium">Wins</td>
                      {getSelectedTeamData().map((team, index) => (
                        <td key={index} className="px-4 py-3 text-center text-green-400 font-bold text-lg">{team.wins}</td>
                      ))}
                    </tr>
                    <tr className="hover:bg-slate-800/30">
                      <td className="px-4 py-3 text-slate-400 font-medium">Draws</td>
                      {getSelectedTeamData().map((team, index) => (
                        <td key={index} className="px-4 py-3 text-center text-yellow-400 font-bold text-lg">{team.draws}</td>
                      ))}
                    </tr>
                    <tr className="hover:bg-slate-800/30">
                      <td className="px-4 py-3 text-slate-400 font-medium">Losses</td>
                      {getSelectedTeamData().map((team, index) => (
                        <td key={index} className="px-4 py-3 text-center text-red-400 font-bold text-lg">{team.losses}</td>
                      ))}
                    </tr>
                    <tr className="hover:bg-slate-800/30">
                      <td className="px-4 py-3 text-slate-400 font-medium">Goals For</td>
                      {getSelectedTeamData().map((team, index) => (
                        <td key={index} className="px-4 py-3 text-center text-white">{team.goalsFor}</td>
                      ))}
                    </tr>
                    <tr className="hover:bg-slate-800/30">
                      <td className="px-4 py-3 text-slate-400 font-medium">Goals Against</td>
                      {getSelectedTeamData().map((team, index) => (
                        <td key={index} className="px-4 py-3 text-center text-white">{team.goalsAgainst}</td>
                      ))}
                    </tr>
                    <tr className="hover:bg-slate-800/30">
                      <td className="px-4 py-3 text-slate-400 font-medium">Possession %</td>
                      {getSelectedTeamData().map((team, index) => (
                        <td key={index} className="px-4 py-3 text-center text-white">{team.possession}%</td>
                      ))}
                    </tr>
                    <tr className="hover:bg-slate-800/30">
                      <td className="px-4 py-3 text-slate-400 font-medium">Pass Accuracy %</td>
                      {getSelectedTeamData().map((team, index) => (
                        <td key={index} className="px-4 py-3 text-center text-white">{team.passAccuracy}%</td>
                      ))}
                    </tr>
                    <tr className="hover:bg-slate-800/30">
                      <td className="px-4 py-3 text-slate-400 font-medium">Shots per Game</td>
                      {getSelectedTeamData().map((team, index) => (
                        <td key={index} className="px-4 py-3 text-center text-white">{team.shotsPerGame}</td>
                      ))}
                    </tr>
                    <tr className="hover:bg-slate-800/30">
                      <td className="px-4 py-3 text-slate-400 font-medium">Team Rating</td>
                      {getSelectedTeamData().map((team, index) => (
                        <td key={index} className="px-4 py-3 text-center">
                          <span className="px-3 py-1 bg-yellow-600/20 text-yellow-400 font-bold rounded-full">
                            {team.rating}
                          </span>
                        </td>
                      ))}
                    </tr>
                  </tbody>
                </table>
              </div>
            </div>

            {/* Bar Chart Comparison */}
            <div className="bg-gradient-to-br from-slate-800 to-slate-900 rounded-2xl p-6 border border-slate-700/50 shadow-xl">
              <h3 className="text-lg font-semibold text-blue-400 mb-6 flex items-center space-x-2">
                <Target className="w-5 h-5" />
                <span>Key Metrics Comparison</span>
              </h3>
              <ResponsiveContainer width="100%" height={300}>
                <BarChart data={teamBarChartData}>
                  <CartesianGrid strokeDasharray="3 3" stroke="#334155" />
                  <XAxis dataKey="metric" stroke="#94a3b8" />
                  <YAxis stroke="#94a3b8" />
                  <Tooltip 
                    contentStyle={{ 
                      backgroundColor: '#1e293b', 
                      border: '1px solid #475569', 
                      borderRadius: '8px' 
                    }}
                    labelStyle={{ color: '#e2e8f0' }}
                  />
                  <Legend 
                    wrapperStyle={{ paddingTop: '20px' }}
                    iconType="circle"
                  />
                  {getSelectedTeamData().map((team, index) => (
                    <Bar 
                      key={team.name} 
                      dataKey={team.name} 
                      fill={colors[index]} 
                      radius={[8, 8, 0, 0]}
                    />
                  ))}
                </BarChart>
              </ResponsiveContainer>
            </div>

            {/* Radar Chart - Team Fingerprint */}
            <div className="bg-gradient-to-br from-slate-800 to-slate-900 rounded-2xl p-6 border border-slate-700/50 shadow-xl">
              <h3 className="text-lg font-semibold text-blue-400 mb-6 flex items-center space-x-2">
                <Activity className="w-5 h-5" />
                <span>Team Performance Fingerprint</span>
              </h3>
              <ResponsiveContainer width="100%" height={400}>
                <RadarChart data={teamRadarData}>
                  <PolarGrid stroke="#475569" />
                  <PolarAngleAxis dataKey="attribute" stroke="#94a3b8" />
                  <PolarRadiusAxis angle={90} domain={[0, 100]} stroke="#94a3b8" />
                  <Tooltip 
                    contentStyle={{ 
                      backgroundColor: '#1e293b', 
                      border: '1px solid #475569', 
                      borderRadius: '8px' 
                    }}
                  />
                  <Legend 
                    wrapperStyle={{ paddingTop: '20px' }}
                    iconType="circle"
                  />
                  {getSelectedTeamData().map((team, index) => (
                    <Radar
                      key={team.name}
                      name={team.name}
                      dataKey={team.name}
                      stroke={colors[index]}
                      fill={colors[index]}
                      fillOpacity={0.3}
                      strokeWidth={2}
                    />
                  ))}
                </RadarChart>
              </ResponsiveContainer>
            </div>

            {/* Head-to-Head Stats Card */}
            <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
              {getSelectedTeamData().map((team, index) => (
                <div key={index} className="bg-gradient-to-br from-slate-800 to-slate-900 rounded-2xl p-6 border border-slate-700/50 shadow-xl">
                  <div className="flex items-center space-x-3 mb-6">
                    <div className={`w-12 h-12 rounded-lg flex items-center justify-center`} style={{ backgroundColor: colors[index] + '33' }}>
                      <Shield className="w-6 h-6" style={{ color: colors[index] }} />
                    </div>
                    <h3 className="text-xl font-bold text-white">{team.name}</h3>
                  </div>
                  
                  <div className="space-y-4">
                    <div className="flex items-center justify-between">
                      <span className="text-slate-400 text-sm">Win Rate</span>
                      <span className="text-white font-bold">
                        {Math.round((team.wins / (team.wins + team.draws + team.losses)) * 100)}%
                      </span>
                    </div>
                    <div className="w-full bg-slate-700 rounded-full h-2">
                      <div 
                        className="h-2 rounded-full" 
                        style={{ 
                          width: `${Math.round((team.wins / (team.wins + team.draws + team.losses)) * 100)}%`,
                          backgroundColor: colors[index]
                        }}
                      ></div>
                    </div>
                    
                    <div className="grid grid-cols-2 gap-4 pt-4">
                      <div className="text-center p-3 bg-slate-800/50 rounded-lg">
                        <p className="text-slate-400 text-xs mb-1">Goal Diff</p>
                        <p className="text-2xl font-bold text-green-400">+{team.goalsFor - team.goalsAgainst}</p>
                      </div>
                      <div className="text-center p-3 bg-slate-800/50 rounded-lg">
                        <p className="text-slate-400 text-xs mb-1">Form</p>
                        <p className="text-2xl font-bold" style={{ color: colors[index] }}>
                          {team.rating}
                        </p>
                      </div>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}

        {/* Analysis Insights Card */}
        <div className="bg-gradient-to-br from-blue-900/20 to-slate-900 rounded-2xl p-6 border border-blue-700/30 shadow-xl">
          <div className="flex items-start space-x-4">
            <div className="w-12 h-12 bg-blue-600/20 rounded-lg flex items-center justify-center flex-shrink-0">
              <Zap className="w-6 h-6 text-blue-400" />
            </div>
            <div>
              <h3 className="text-lg font-bold text-white mb-2">AI Analysis Insights</h3>
              <p className="text-slate-400 text-sm leading-relaxed">
                {activeTab === 'players' ? (
                  <>
                    Based on the comparison, <strong className="text-blue-400">{getSelectedPlayerData()[0]?.name}</strong> excels in offensive metrics with superior goal-scoring ability, 
                    while <strong className="text-blue-400">{getSelectedPlayerData()[1]?.name}</strong> demonstrates stronger playmaking and defensive contributions. 
                    The radar chart reveals complementary skill sets that could work effectively in tandem on the field.
                  </>
                ) : (
                  <>
                    <strong className="text-blue-400">{getSelectedTeamData()[0]?.name}</strong> shows a more aggressive attacking approach with higher goals scored, 
                    while <strong className="text-blue-400">{getSelectedTeamData()[1]?.name}</strong> maintains a more balanced defensive structure. 
                    The possession and pass accuracy metrics indicate different tactical philosophies between the teams.
                  </>
                )}
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default ComparisonPage;