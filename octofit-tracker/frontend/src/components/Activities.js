import React, { useEffect, useState } from 'react';

function Activities() {
  const [activities, setActivities] = useState([]);

  useEffect(() => {
    fetch('https://opulent-space-orbit-969wg6g9pxh7r5x-8000.app.github.dev/api/activities/')
      .then(response => response.json())
      .then(data => setActivities(data))
      .catch(error => console.error('Error fetching activities:', error));
  }, []);

  return (
    <div className="card">
      <div className="card-body">
        <h1 className="card-title text-center">Activities</h1>
        <table className="table table-striped">
          <thead>
            <tr>
              <th>User</th>
              <th>Activity Type</th>
              <th>Duration</th>
              <th>Points</th>
            </tr>
          </thead>
          <tbody>
            {activities.map(activity => (
              <tr key={activity._id}>
                <td>{activity.user ? activity.user.username : 'Unknown User'}</td>
                <td>{activity.activity_type}</td>
                <td>{activity.duration} minutes</td>
                <td>{activity.points}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}

export default Activities;
