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

## Cài đặt

### Cowork

Thêm marketplace từ repo này (`pichu124/casa-plugins`) trong phần quản lý plugin của tổ chức, rồi bật các plugin cần dùng.

### Claude Code

```bash
claude plugin marketplace add pichu124/casa-plugins
claude plugin install casa-ops@casa-plugins
```

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
