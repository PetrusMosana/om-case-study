locals {
  files = {
    "0" = "file0.txt"
    "2" = "file2.txt"
    "3" = "file3.txt"
    "4" = "file4.txt"
  }
}

resource "local_file" "foo" {
  for_each = local.files

  content  = "# Some content for file ${each.key}"
  filename = each.value
}