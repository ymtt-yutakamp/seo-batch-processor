#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
全186行を「自社サービス公式サイト」か「比較・まとめ記事（第三者サイト）」に分類する。
URLごとに人手でレビューした結果をマッピングとして適用する。
URLが「取得不可」の行は、比較記事内から個別企業として抽出された行のため
「自社サービス（URL不明）」として扱う（企業自体は実在する候補のため）。
"""
import json
from pathlib import Path

RESULTS_JSON = Path(__file__).parent / "data" / "results.json"

OWN = "自社サービス公式サイト"
OWN_NO_URL = "自社サービス（URL不明）"
COMPARISON = "比較・まとめ記事（第三者サイト）"

# URL → 分類
URL_CLASSIFICATION = {
    "https://www.plan-b.co.jp/blog/seo/85288/": COMPARISON,
    "https://www.aidma-hd.jp/ai/ai-lighting/": COMPARISON,
    "https://digitalidentity.co.jp/blog/seo/article-creation-agency.html": COMPARISON,
    "https://seo-writing-professionals.com/": OWN,
    "https://www.canva.com/ja_jp/features/ai-kiji/": OWN,
    "https://www.aspicjapan.org/asu/article/41612": COMPARISON,
    "https://lead-x.co.jp/seo/ai-seo-writing/": OWN,
    "https://counter-digital.jp/service/ai/": OWN,
    "https://boater.jp/article/1444": COMPARISON,
    "https://n-works.link/blog/marketing/5-ai-article-creation-tools": COMPARISON,
    "https://biz.customlife.co.jp/blog/article-creation-costs/": COMPARISON,
    "https://bakuyasu.techsuite.co.jp/": OWN,
    "https://www.geo-code.co.jp/seo/mag/writing-agency/": COMPARISON,
    "https://www.value-domain.com/value-aiwriter/": OWN,
    "https://takuwil.spool.co.jp/column/article/seo-article-production-agency/": COMPARISON,
    "https://white-link.com/sem-plus/content-writing-agency/": COMPARISON,
    "https://stock-sun.com/column/seo-articles-request/": COMPARISON,
    "https://kigyolog.com/service.php?id=88": COMPARISON,
    "https://btobmarketing-textbook.com/seo-article-cost/": COMPARISON,
    "https://likg.co.jp/service/article-production/": OWN,
    "https://fungry.co.jp/cnaps/blog/sentence-generation-ai/": COMPARISON,
    "https://www.protea-inc.co.jp/sub-media/ai-article-writing/": COMPARISON,
    "https://web-kanji.com/posts/content-service-compare": COMPARISON,
    "https://xn--3kq3hlnz13dlw7bzic.jp/": OWN,
    "https://stock-sun.com/column/article-production-agency-market-price/": COMPARISON,
    "https://subsc-designoffice.jp/writing/": OWN,
    "https://ai-keiei.shift-ai.co.jp/ai-article-generator-free/": COMPARISON,
    "https://web-kanji.com/posts/seo-price": COMPARISON,
    "https://generative-ai.sejuku.net/blog/1051/": COMPARISON,
    "https://seo.tsukrel.jp/article/1818/": OWN,
    "https://www.propagateinc.com/post/ai-article-writing-service": OWN,
    "https://mokumoku.works/": OWN,
    "https://anzu-writing.com/": OWN,
    "https://seo-taisacu.jp/writing/": OWN,
    "https://bakuyasu.techsuite.co.jp/30269/": COMPARISON,
    "https://stock-sun.com/column/seo-ai/": COMPARISON,
    "https://digi-mado.jp/category/marketing/seo-tools/": COMPARISON,
    "https://www.willgate.co.jp/promonista/ai-wiriting-tool-recommendation/": COMPARISON,
    "https://www.gohp.jp/blog/website-operation/5360/": COMPARISON,
    "https://n-works.link/blog/seo/seo-article-creation-using-ai-writing": COMPARISON,
    "https://oproduct.ai/articles/3887896": COMPARISON,
    "https://ai-seo.tokyo/lp": OWN,
    "https://dream-up.co.jp/marketing/media/seo-article-agency/": COMPARISON,
    "https://www.itmedia.co.jp/itselect/ai-writing/article/5300/": COMPARISON,
    "https://saas.imitsu.jp/cate-generative-ai": COMPARISON,
    "https://saas.imitsu.jp/cate-generative-ai/article/h-2670": COMPARISON,
    "https://boxil.jp/mag/a10168/": COMPARISON,
    "https://www.itmedia.co.jp/itselect/ai-writing/": COMPARISON,
    "https://saas.imitsu.jp/cate-generative-ai/serviceList": COMPARISON,
    "https://www.aspicjapan.org/asu/article/34648": COMPARISON,
    "https://next-sfa.jp/journal/ai-writing-tool/recommended-ai-writing/": COMPARISON,
    "https://www.leadplus.co.jp/blog/automatically-generate-blog-posts-ai": COMPARISON,
    "https://rakkokeyword.com/techo/ai-suggest-article/": OWN,
    "https://note.com/ihayato/n/n313fcd68336a": COMPARISON,
    "https://pantograph.co.jp/blog/production/ai-writting.html": COMPARISON,
    "https://sakubun.ai/blog/ai-blog-auto-creation-tool": COMPARISON,
    "https://homepage-cube.com/column/ai%E3%81%AB%E3%82%88%E3%82%8B%E8%A8%98%E4%BA%8B%E8%87%AA%E5%8B%95%E4%BD%9C%E6%88%90%E3%82%B5%E3%83%BC%E3%83%93%E3%82%B9%E3%80%8Carticoolo%E3%80%8D%E3%82%92%E8%A9%A6%E3%81%97%E3%81%A6%E3%81%BF%E3%81%9F/": COMPARISON,
    "https://search-engine-pirates.co.jp/column/content-seo/seo-article-price/": COMPARISON,
    "https://seo-writing-professionals.com/writing-outsourcing/": COMPARISON,
    "https://lead-x.co.jp/column/ai-seo-column/": COMPARISON,
    "https://ai-writer.jp/": OWN,
    "https://n-works.link/writing": OWN,
    "https://www.seohacks.net/service/content-marketing-production/": OWN,
    "https://n-works.link/blog/seo/article-creation-using-generative-ai": COMPARISON,
    "https://www.lany.co.jp/service/digitalmarketing/writing": OWN,
    "https://wacul.co.jp/service/seo-content": OWN,
    "https://www.plan-b.co.jp/solution/seo/content/": OWN,
    "https://search-engine-pirates.co.jp/seo-article-production-agency/": OWN,
    "https://japan-ai.co.jp/media/1897/": COMPARISON,
    "https://simplique.jp/about-generative-ai-tools-for-article-creation/": COMPARISON,
    "https://help-you.me/blog/articles_writing/": COMPARISON,
    "https://saas.imitsu.jp/cate-generative-ai/article/l-2416": COMPARISON,
    "https://note.com/shushuitie/n/n103038ca53cf": COMPARISON,
    "https://simplique.jp/free-ai-writing-tools/": COMPARISON,
    "https://n-works.link/blog/seo/free-ai-writing-tool": COMPARISON,
    "https://white-link.com/sem-plus/ai-writing-tools/": COMPARISON,
    "https://www.jenova.ai/ja/resources/ai-story-generator-free-unlimited-no-restrictions": OWN,
    "https://ai-writing.tech/ai-writing/": COMPARISON,
    "https://n-v-l.co/blog/ai-writing-tool-free": COMPARISON,
    "https://www.seohacks.net/blog/20719/": COMPARISON,
    "https://n-works.link/blog/seo/seo-rating-points": COMPARISON,
    "https://www.conmark.jp/column/seo-contents": COMPARISON,
    "https://leadnine.co.jp/media-seo/6417/": COMPARISON,
    "https://article-pro.com/column/foundation/seo-articles/": COMPARISON,
    "https://cone-c-slide.com/see-sla/blog/article-price/": COMPARISON,
    "https://shwat.jp/ultra/price/": OWN,
    "https://sts-d.com/blog/web-content/content-basics/article-agency-market-price/": COMPARISON,
    "https://www.lancers.jp/menu/browse/writing_translation/ai_writing": COMPARISON,
    "https://note.com/hiro_seki/n/na7335f0c71ba": COMPARISON,
    "https://cro-co.co.jp/media/seo/article-creation-ai/": COMPARISON,
    "https://linkeeps.com/ai-services/": COMPARISON,
    "https://www.street-academy.com/seo-skill/services/subscription": COMPARISON,
    "https://withstyle-web.com/column/maintenance/%E3%82%B5%E3%83%96%E3%82%B9%E3%82%AF%E5%9E%8B%E3%83%9B%E3%83%BC%E3%83%A0%E3%83%9A%E3%83%BC%E3%82%B8%E5%88%B6%E4%BD%9C%E3%81%A7seo%E5%AF%BE%E7%AD%96%E3%81%AF%E3%81%A7%E3%81%8D%E3%82%8B%E3%81%AE/": COMPARISON,
    "https://www.siteengine.co.jp/blog/contents-cost/": COMPARISON,
    "https://www.lancers.jp/menu/tag/%E3%82%B3%E3%83%B3%E3%83%86%E3%83%B3%E3%83%84%E5%88%B6%E4%BD%9C": OWN,
    "https://cloudcircus.jp/consultinglp/contentcreation/": OWN,
    "https://appmart.co.jp/content-marketing/": OWN,
    "https://takuwil.spool.co.jp/column/article/content-production-company/": COMPARISON,
    "https://shwat.jp/ultra/content-production-company/": COMPARISON,
    "https://seo-writing-professionals.com/content-production-company/": COMPARISON,
    "https://kgc-c.co.jp/b-mag/2248": COMPARISON,
    "https://artbrains.co.jp/article/generative-ai/3652/": COMPARISON,
    "https://www.lancers.jp/menu/tag/SEO%E8%A8%98%E4%BA%8B%E4%BD%9C%E6%88%90": OWN,
    "https://hnavi.co.jp/knowledge/blog/seo-cost/": COMPARISON,
    "https://coomil.co.jp/column/seowriting-outsourcing/": COMPARISON,
    "https://rank-quest.jp/column/column/writing-outsourcing/": COMPARISON,
    "https://boxil.jp/mag/a4489/": COMPARISON,
    "https://coconala.com/categories/372": OWN,
    "https://fungry.co.jp/cnaps/blog/outsourcing/": COMPARISON,
    "https://crowdworks.jp/public/employees/skill/496": OWN,
    "https://www.lancers.jp/work/search/writing/writing": OWN,
    "https://www.lancers.jp/menu/tag/WEB%E3%83%A9%E3%82%A4%E3%83%86%E3%82%A3%E3%83%B3%E3%82%B0": OWN,
    "https://enterprise.goworkship.com/lp/writer/how-to-search": OWN,
    "https://works.sagooo.com/order/": OWN,
    "https://note.com/cannele_writing/n/n0b607441c24b": COMPARISON,
    "https://righting.co.jp/": OWN,
    "https://www.conmark.jp/column/seo-content-cost": COMPARISON,
    "https://sider-story.co.jp/knowledge/seo-contents-price/": COMPARISON,
    "https://counter-digital.jp/counter-media/article-writing-outsourcing/": COMPARISON,
    "https://sts-d.com/blog/web-content/acquisition/seo-price/": COMPARISON,
    "https://help-you.me/blog/ai-writing/": COMPARISON,
    "https://bltz.co.jp/write-text-tool-ai/": COMPARISON,
    "https://leap-me.com/ja/app/text-generator": OWN,
    "https://www.onamae.com/business/article/67453/": COMPARISON,
    "https://subsc-designoffice.jp/blog/contents/comparison-2/": COMPARISON,
    "https://subsc-designoffice.jp/blog/contents/article-writing-fee/": COMPARISON,
}


def classify(row):
    url = row["URL"]
    if url == "取得不可":
        return OWN_NO_URL
    if url in URL_CLASSIFICATION:
        return URL_CLASSIFICATION[url]
    # 未知のURL（想定外）は安全側に倒して比較記事扱いにする
    return COMPARISON + "（要確認）"


def main():
    with open(RESULTS_JSON, encoding="utf-8") as f:
        data = json.load(f)

    counts = {}
    for row in data:
        c = classify(row)
        row["サイト種別"] = c
        counts[c] = counts.get(c, 0) + 1

    with open(RESULTS_JSON, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print("分類結果:")
    for k, v in sorted(counts.items(), key=lambda x: -x[1]):
        print(f"  {k}: {v}件")
    print(f"合計: {len(data)}件")


if __name__ == "__main__":
    main()
