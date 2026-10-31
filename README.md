# casa-plugins

Kho plugin Claude nội bộ của **Casa dei Bambini**, hệ thống trường mầm non ở Hà Nội gồm 3 cơ sở: Quốc tế Chùa Láng, Quốc tế Mỹ Đình và Song ngữ Kim Mã.

Kho này sao từ [anthropics/knowledge-work-plugins](https://github.com/anthropics/knowledge-work-plugins), giấy phép Apache 2.0 (xem [LICENSE](LICENSE)). Những thay đổi so với bản gốc: bỏ các plugin không phù hợp với trường, bỏ toàn bộ plugin bên ngoài và các workflow phục vụ chúng, thêm plugin `casa-ops`.

## Plugin

| Plugin | Dùng cho | Ghi chú |
|---|---|---|
| **[casa-ops](./casa-ops)** | Bối cảnh Casa, báo cáo lead tuần, gợi ý nội dung từ câu phụ huynh hỏi, rà soát hỏi đáp của bot | Của Casa. Đọc bối cảnh ở đây trước khi dùng plugin khác |
| [productivity](./productivity) | Quản lý việc, lịch, ghi nhớ bối cảnh công việc | Bản gốc |
| [marketing](./marketing) | Soạn nội dung, lên chiến dịch, báo cáo hiệu quả | Bản gốc |
| [sales](./sales) | Chăm sóc lead: chuẩn bị cuộc gọi, soạn tin theo dõi, rà pipeline | Bản gốc |
| [customer-support](./customer-support) | Soạn trả lời, xử lý khiếu nại, viết bài hỏi đáp | Bản gốc |
| [operations](./operations) | Quy trình, báo cáo vận hành, nhà cung cấp | Bản gốc |
| [human-resources](./human-resources) | Tuyển dụng, đánh giá, chính sách nhân sự | Bản gốc. Các nội dung luật lao động theo Mỹ cần đối chiếu với luật Việt Nam |
| [pdf-viewer](./pdf-viewer) | Xem, ghi chú, ký PDF (hợp đồng, đơn nhập học) | Bản gốc |
| [cowork-plugin-management](./cowork-plugin-management) | Tạo và chỉnh plugin | Bản gốc |

Các plugin gốc viết theo chuẩn Mỹ. Khi làm việc cho Casa, dùng tiếng Việt, tiền VND, quy định Việt Nam và giọng văn với phụ huynh như mô tả trong [`casa-ops/references/boi-canh-casa.md`](casa-ops/references/boi-canh-casa.md).

## Cài đặt (làm một lần)

Plugin được cài từ nhánh `main`, nên chỉ dùng được những gì đã gộp vào `main`.

### 1. Thêm kho plugin

**Cowork / claude.ai:** vào phần quản lý plugin, thêm marketplace từ GitHub và chọn repo `pichu124/casa-plugins`, rồi bật các plugin cần dùng. Repo để riêng tư, nên tài khoản GitHub phải kết nối với Claude rồi mới thêm được.

**Claude Code (máy tính):**

```bash
claude plugin marketplace add pichu124/casa-plugins
claude plugin install casa-ops@casa-plugins
claude plugin install sales@casa-plugins   # các plugin khác cài tương tự
```

### 2. Kết nối Google Sheets và Google Drive

Vào **Cài đặt → Connectors** trên claude.ai, đăng nhập bằng tài khoản Google có quyền xem Sheet lead. Chưa kết nối thì có thể xuất Sheet ra `.xlsx` hoặc `.csv` rồi tải lên cho Claude.

## Cách dùng

Có hai cách gọi:

- **Hỏi bằng tiếng Việt bình thường.** Claude tự chọn skill phù hợp, ví dụ "Tuần rồi có bao nhiêu lead?".
- **Gọi đích danh** bằng `/tên-plugin:tên-skill`, ví dụ `/casa-ops:bao-cao-tuan`.

### casa-ops

| Skill | Gọi | Ví dụ |
|---|---|---|
| Báo cáo tuần | `/casa-ops:bao-cao-tuan` | "Báo cáo lead tuần trước", "So sánh lead tuần này với tuần trước" |
| Chủ đề → nội dung | `/casa-ops:chu-de-noi-dung` | "30 ngày qua phụ huynh hỏi gì nhiều nhất? Gợi ý bài đăng cho Mỹ Đình" |
| Rà soát hỏi đáp | `/casa-ops:ra-soat-hoi-dap` | "Hai tuần qua bot phải chuyển tư vấn viên những câu nào? Soạn câu trả lời mới để trường duyệt" |

Lần đầu dùng, gửi link Google Sheet lead cho Claude. Ba skill này hiện mới là khung: chạy được và tính đúng các chỉ số đã thống nhất, nhưng cách trình bày chưa cố định. Báo cáo tự chạy lúc 8h sáng thứ Hai sẽ được cài sau.

### Các plugin gốc

Các plugin này viết theo kiểu doanh nghiệp Mỹ. Khi dùng, nên nói thêm "theo bối cảnh Casa", để Claude lấy cơ sở, học phí và giọng văn xưng "em", gọi "Ba/Mẹ" từ `casa-ops`.

| Plugin | Skill hay dùng | Ví dụ |
|---|---|---|
| sales | `draft-outreach`, `call-prep`, `lead-triage`, `pipeline-review` | "Soạn tin Zalo hỏi thăm Mẹ bé An sau buổi tham quan" · "Chuẩn bị gọi cho phụ huynh đang băn khoăn học phí Mỹ Đình" |
| marketing | `content-creation`, `campaign-plan`, `performance-report` | "Lên kế hoạch quảng cáo tuyển sinh tháng 12 cho Kim Mã" |
| customer-support | `draft-response`, `customer-escalation`, `kb-article` | "Soạn trả lời phụ huynh phàn nàn bé bị trầy ở lớp" |
| productivity | `start`, `task-management`, `memory-management` | "Hôm nay tôi cần làm gì?" · "Nhớ giúp: cơ sở Kim Mã nghỉ ngày 20/11" |
| operations | `process-doc`, `status-report`, `vendor-review` | "Viết quy trình đón trả bé muộn sau 17h30" |
| human-resources | `interview-prep`, `onboarding`, `draft-offer` | "Câu hỏi phỏng vấn giáo viên mầm non có bằng cao đẳng sư phạm" |
| pdf-viewer | `view-pdf` | "Mở hợp đồng nhập học này và đánh dấu điều khoản bảo lưu" |
| cowork-plugin-management | `cowork-plugin-customizer`, `create-cowork-plugin` | Dùng để chỉnh hoặc tạo plugin mới |

Với human-resources, phần lương, hợp đồng và luật lao động viết theo luật Mỹ, cần đối chiếu với Bộ luật Lao động Việt Nam trước khi dùng.

### Nguyên tắc khi dùng

- Plugin chỉ đọc dữ liệu và soạn bản nháp. Không tự nhắn phụ huynh, không nhắc tư vấn viên vì bot Messenger đã làm phần này.
- Báo cáo chỉ ghi tên kèm 4 số cuối SĐT.
- Nội dung Claude soạn để gửi phụ huynh, người dùng đọc lại trước khi gửi.

## Cấu trúc một plugin

```
ten-plugin/
├── .claude-plugin/plugin.json   # Khai báo plugin
├── .mcp.json                    # Connector (MCP server)
├── commands/                    # Lệnh gọi trực tiếp (nếu có)
└── skills/                      # Kiến thức và quy trình Claude tự dùng khi phù hợp
```

## Quy tắc

- Sửa trên nhánh riêng và mở Pull Request. Không push thẳng lên `main`.
- Không đưa dữ liệu thật của phụ huynh và trẻ (tên, SĐT, tin nhắn) vào repo, commit hay PR.
