#!/bin/bash

echo "📺 Starting Live Logs (All Services)..."
echo "----------------------------------------"

# 1. اجرای لاگ‌ها در پس‌زمینه (برای همه سرویس‌ها)
# این دستور لاگ پارسر، جمع، ضرب و پرانتز رو همزمان نشون میده
kubectl logs -f -l 'app in (parser, add-sub, mult-div, paren)' --all-containers=true --prefix --tail=0 --max-log-requests=20 &
LOG_PID=$! # ذخیره شناسه پروسه لاگ برای بستن در آخر

# کمی صبر برای لود شدن لاگ‌ها
sleep 2
echo "----------------------------------------"
echo "🚀 Starting Load Test (Targeting: Parser + Add/Sub + Mult/Div)..."

# 2. اجرای تست فشار (همزمان)
kubectl run bench-test --rm -i --tty --image=curlimages/curl --restart=Never -- /bin/sh -c '
  start_time=$(date +%s)

  # ارسال ۵ درخواست همزمان (تعداد رو کم کردیم که لاگ‌ها قاطی نشن)
  for i in $(seq 1 5); do
    # عبارت شامل جمع و ضرب است تا همه سرویس‌ها درگیر شوند
    curl -s -o /dev/null -X POST http://parser-service:5000/parse \
      -H "Content-Type: application/json" \
      -d "{\"expression\": \"20*3+4\"}" &
  done

  wait
  end_time=$(date +%s)
  duration=$((end_time - start_time))
  echo "----------------------------------------"
  echo "✅ Finished in: $duration seconds"
'
