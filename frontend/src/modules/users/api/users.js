import api from '@/api/axios'

export const registerUser = (data) => {
  return api.post('/users/register/', data)
}

export const loginUser = (data) => {
  return api.post('/auth/login/', data)
}

export const getProfile = () => {
  return api.get('/users/profile/')
}

export const updateProfile = (data) => {
  return api.patch('/users/profile/', data)
}

export const updateLocation = (data) => {
  return api.post('/users/location/', data)
}

export const changePassword = (data) => {
  return api.post('/users/change-password/', data)
}

export const deleteAccount = () => {
  return api.delete('/users/delete/')
}

export const requestPasswordReset = (data) => {
  return api.post('/users/password-reset/', data)
}

export const confirmPasswordReset = (data) => {
  return api.post('/users/password-reset/confirm/', data)
}

export const logoutUser = () => {
  return api.post('/auth/logout/');
}