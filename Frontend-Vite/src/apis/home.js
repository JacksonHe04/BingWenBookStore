import httpInstance from '@/utils/http'


// 获取banner

export function getBannerAPI (params = {}) {
  // 默认为1 商品为2
  const { distributionSite = '1' } = params
  return httpInstance({
    url: '/home/banner',
    params: {
      distributionSite
    }
  })
}

/**
 * @description: 获取新鲜好物
 * @param {*}
 * @return {*}
 */
export const findNewAPI = () => {
  return httpInstance({
    url: '/home/new'
  })
}

/**
 * @description: 获取推荐作家
 * @param {*}
 * @return {*}
 */
export const getAuthorAPI = () => {
  return httpInstance({
    url: '/home/brand'
  })
}

/**
 * @description: 获取人气推荐
 * @param {*}
 * @return {*}
 */
export const getHotAPI = () => {
  return httpInstance({
    url: '/home/hot'
  })
}

/**
 * @description: 获取所有商品模块
 * @param {*}
 * @return {*}
 */
export const getGoodsAPI = () => {
  return httpInstance({
    url: '/home/goods'
  })
}

/**
 * @description: 搜索书籍
 * @param {string} query - 搜索关键词
 * @return {Promise}
 */
export const searchBooksAPI = (query) => {
  return httpInstance({
    url: '/product/search',
    params: {
      query
    }
  })
}
