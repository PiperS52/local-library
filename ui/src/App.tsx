import './App.css';
import { Provider } from 'react-redux';
import { setupStore } from './store';
import { setupListeners } from '@reduxjs/toolkit/query';
import { WishlistsPage } from './pages/WishlistsPage';
import { Navigate, Route, Routes } from 'react-router';

const store = setupStore();
setupListeners(store.dispatch);

function App() {
  return (
    <>
      <Provider store={store}>
        <Routes>
          <Route
            path="/"
            element={<Navigate replace to="/wishlists" />}
          ></Route>
          <Route path="wishlists" element={<WishlistsPage />} />
        </Routes>
      </Provider>
    </>
  );
}

export default App;
