import axios from 'axios';

const login = async () => {
  const res = await axios.post('/login', {
    username: 'admin',
    password: 'raspberry'
  });
  localStorage.setItem('token', res.data.access_token);
};

export default login;
