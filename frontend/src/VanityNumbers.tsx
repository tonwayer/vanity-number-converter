// src/VanityNumbers.tsx
import React, { useState, useEffect } from 'react';
import axios from 'axios';

interface VanityNumber {
  PhoneNumber: string;
  VanityNumbers: string[];
}

const VanityNumbers: React.FC = () => {
  const [vanityNumbers, setVanityNumbers] = useState<VanityNumber[]>([]);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchVanityNumbers = async () => {
      try {
        const response = await axios.get('https://6l7trs2h53.execute-api.us-east-1.amazonaws.com/Prod/vanitynumbers');
        setVanityNumbers(response.data);
        setLoading(false);
      } catch (err) {
        setError("Error");
        setLoading(false);
      }
    };

    fetchVanityNumbers();
  }, []);

  if (loading) return <p>Loading...</p>;
  if (error) return <p>Error loading data: {error}</p>;

  return (
    <div>
      <h1>Vanity Numbers from the Last 5 Callers</h1>
      <table>
        <thead>
          <tr>
            <th>Phone Number</th>
            <th>Vanity Numbers</th>
          </tr>
        </thead>
        <tbody>
          {vanityNumbers.map((item) => (
            <tr key={item.PhoneNumber}>
              <td>{item.PhoneNumber}</td>
              <td>{item.VanityNumbers.join(', ')}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default VanityNumbers;
