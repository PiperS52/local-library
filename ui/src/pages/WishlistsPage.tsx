import { useGetWishlistsQuery } from '../services/wishlists';
import Box from '@mui/material/Box';
import CircularProgress from '@mui/material/CircularProgress';
import { WishlistsGrid } from '../components/WishlistsGrid';

export const WishlistsPage: React.FC = () => {

  const { bookWishlists, isLoading, isError } =
    useGetWishlistsQuery(
      { userId: '1' }, // Replace with actual user ID & move to headers once authentication is implemented
      {
        selectFromResult: ({ data, isLoading, isError }) => ({
          bookWishlists: data ?? [],
          isLoading,
          isError,
        }),
        refetchOnMountOrArgChange: true,
      }
    );

  return (
    <>
      <div>
        <h1>Books wishlist</h1>
        {isLoading && (
          <Box sx={{ display: 'flex' }}>
            <CircularProgress />
          </Box>
        )}
        {isError && <p>Error loading books wishlist</p>}
        {!bookWishlists.length ? (
          <p>No books in wishlist found</p>
        ) : (
          <WishlistsGrid bookWishlists={bookWishlists} />
        )}
      </div>
    </>
  );
};
