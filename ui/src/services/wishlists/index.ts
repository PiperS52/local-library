import { BookWishlistItem } from './types';
import { api } from '../api';

export const wishlistsApi = api.injectEndpoints({
  endpoints: (build) => ({
    getWishlists: build.query<
      BookWishlistItem[],
      {
        userId: string;
      }
    >({
      query: ({ userId }) => ({
        url: `/wishlists`,
        method: 'GET',
        params: { userId },
      }),
      providesTags: ['Wishlists'],
    }),
  }),
  overrideExisting: false,
});

export const { useGetWishlistsQuery, useLazyGetWishlistsQuery } =
  wishlistsApi;
