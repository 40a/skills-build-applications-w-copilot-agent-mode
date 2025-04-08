import React, { useEffect, useState } from 'react';

function Teams() {
  const [teams, setTeams] = useState([]);

  useEffect(() => {
    fetch('https://opulent-space-orbit-969wg6g9pxh7r5x-8000.app.github.dev/api/teams/')
      .then(response => response.json())
      .then(data => setTeams(data))
      .catch(error => console.error('Error fetching teams:', error));
  }, []);

  return (
    <div className="card">
      <div className="card-body">
        <h1 className="card-title text-center">Teams</h1>
        <table className="table table-striped">
          <thead>
            <tr>
              <th>Team Name</th>
              <th>Members</th>
              <th>Total Points</th>
            </tr>
          </thead>
          <tbody>
            {teams.map(team => (
              <tr key={team._id}>
                <td>{team.name}</td>
                <td>{team.members ? team.members.map(member => member.username).join(', ') : 'No members'}</td>
                <td>{team.total_points || 0}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}

export default Teams;
