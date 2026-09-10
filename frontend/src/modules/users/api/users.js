import api from '@/api/axios'

export const registerUser = (data) => {
  return api.post('/users/', data)
}

export const loginUser = (data) => {
  return api.post('/auth/login/', data)
}

export const getProfile = () => {
  return api.get('/users/profile/')
}

export const getPublicProfile = (userId) => {
  return api.get(`/users/${userId}/`)
}

// export const updateProfile = (data) => {
//   return api.patch('/users/profile/', data)
// }
export const updateProfile = (userId, data) => {
  return api.put(`/users/${userId}/`, data)
}

export const updateLocation = (data) => {
  return api.post('/users/location/', data)
}

// export const changePassword = (data) => {
//   return api.post('/users/change-password/', data)
// }

export const deleteAccount = (userId) => {
  return api.delete(`/users/${userId}/`)
}

export const requestPasswordReset = (data) => {
  return api.post('/auth/password-reset/request/', data)
}

export const confirmPasswordReset = (data) => {
  return api.post('/auth/password-reset/confirm/', data)
}

export const confirmEmail = (token) => {
  return api.post('/auth/confirm-email/', { token })
}

export const logoutUser = () => {
  return api.post('/auth/logout/');
}