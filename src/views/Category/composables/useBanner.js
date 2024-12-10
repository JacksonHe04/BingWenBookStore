// 封装banner轮播图相关的业务代码
import { ref, onMounted } from "vue";
import { getBannerAPI } from "@/apis/home";

export function useBanner() {
  const bannerList = ref([]);

  const getBanner = async () => {
    const res = await getBannerAPI({
      distributionSite: "2",
    });
    bannerList.value = res.result;
    console.log("分类页轮播图", bannerList.value);
  };

  onMounted(() => getBanner());

  return {
    bannerList,
  };
}
